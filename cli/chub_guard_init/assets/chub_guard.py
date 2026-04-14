import ast
import datetime
import json
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
import urllib.request
import urllib.error

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.text import Text
from rich.rule import Rule

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

console = Console()

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / ".chub-docs"
REGISTRY_PATH = DOCS_DIR / "registry.json"


@dataclass
class Violation:
    filename: Path
    line: int
    col: int
    code: str
    message: str
    chub_hint: str | None = None
    doc_id: str | None = None


def get_imported_modules(file_path: Path) -> dict[str, list[tuple[int, int]]]:
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(content)
    except SyntaxError as e:
        console.print(f"[yellow]⚠ Warning: Syntax error in {file_path}: {e}. Skipping AST parse.[/yellow]")
        return {}
    except Exception as e:
        console.print(f"[yellow]⚠ Warning: Error parsing {file_path}: {e}. Skipping.[/yellow]")
        return {}

    modules = {}
    lines = content.splitlines()

    def add_mod(name, node):
        line = node.lineno
        # Check for noqa suppression
        if line - 1 < len(lines) and "# noqa: UP" in lines[line - 1]:
            return
        if name not in modules:
            modules[name] = []
        modules[name].append((line, node.col_offset + 1))

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                add_mod(alias.name, node)
                add_mod(alias.name.split(".")[0], node)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                add_mod(node.module, node)
                add_mod(node.module.split(".")[0], node)
    return modules


def extract_chub_hint(doc_path: Path) -> str | None:
    if not doc_path.exists():
        return None
    content = doc_path.read_text(encoding="utf-8", errors="replace")

    in_relevant_section = False
    in_code_block = False
    code_lines = []
    
    # Try to find specific usage sections first
    for line in content.splitlines():
        stripped = line.strip().lower()
        if stripped.startswith("## usage") or stripped.startswith("## core usage") or stripped.startswith("## basic inference") or stripped.startswith("## golden rule") or stripped.startswith("## quickstart"):
            in_relevant_section = True
            continue
        elif line.startswith("## "):
            if in_relevant_section and not in_code_block:
                in_relevant_section = False

        if in_relevant_section:
            if line.strip().startswith("```python") and not in_code_block:
                in_code_block = True
                continue
            elif line.strip().startswith("```") and in_code_block:
                break

            if in_code_block:
                code_lines.append(line)

    # Fallback: if no specific section found, just grab the very first python code block in the document
    if not code_lines:
        in_code_block = False
        for line in content.splitlines():
            if line.strip().startswith("```python") and not in_code_block:
                in_code_block = True
                continue
            elif line.strip().startswith("```") and in_code_block:
                break
                
            if in_code_block:
                code_lines.append(line)

    if code_lines:
        return "\n".join(code_lines)
    return None


@click.group()
def cli():
    pass


@cli.command()
@click.argument("filenames", nargs=-1, type=click.Path(exists=True, path_type=Path))
def run(filenames):
    """Run the pre-commit deprecation guard."""
    py_files = [f for f in filenames if f.suffix == ".py"]
    if not py_files:
        sys.exit(0)

    try:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        console.print(f"[red]Error: Malformed or missing registry.json at {REGISTRY_PATH}: {e}[/red]")
        sys.exit(1)

    file_to_modules = {}
    all_needed_docs = set()
    for f in py_files:
        modules = get_imported_modules(f)
        file_to_modules[f] = modules
        for mod in modules:
            if mod in registry:
                all_needed_docs.add(registry[mod])

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    chub_cmd = shutil.which("chub")
    chub_available = chub_cmd is not None
    if not chub_available:
        console.print("[yellow]⚠ chub unavailable — skipping doc fetch, ruff UP still runs[/yellow]")

    for doc_id in all_needed_docs:
        safe_name = doc_id.replace("/", "__")
        doc_path = DOCS_DIR / f"{safe_name}.md"
        
        needs_fetch = True
        if doc_path.exists():
            mtime = doc_path.stat().st_mtime
            if (time.time() - mtime) < 86400:
                try:
                    rel_path = doc_path.relative_to(REPO_ROOT)
                except ValueError:
                    rel_path = doc_path
                console.print(f"[green]✓ docs cached → {rel_path}[/green]")
                needs_fetch = False

        if needs_fetch:
            success = False
            if chub_available:
                try:
                    res = subprocess.run(
                        [chub_cmd, "get", doc_id, "--lang", "python", "--output", str(doc_path)],
                        timeout=30,
                        capture_output=True,
                        check=False
                    )
                    if res.returncode == 0:
                        success = True
                    else:
                        console.print(f"[yellow]⚠ Warning: chub fetch failed for {doc_id}: {res.stderr.decode('utf-8', errors='replace')}. Falling back to GitHub raw fetch...[/yellow]")
                except Exception as e:
                    console.print(f"[yellow]⚠ Warning: chub fetch timed out or failed for {doc_id}: {e}. Falling back to GitHub raw fetch...[/yellow]")

            if not success:
                # Fallback to direct raw github download since chub CLI crashes on some packages in Windows
                try:
                    # Parse package format: e.g., "openai/package", "langchain/core", "gemini/genai"
                    parts = doc_id.split("/")
                    if len(parts) == 2:
                        pkg, doc = parts
                        url = f"https://raw.githubusercontent.com/andrewyng/context-hub/main/content/{pkg}/docs/{doc}/python/DOC.md"
                        
                        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req, timeout=15) as response:
                            doc_path.write_bytes(response.read())
                        console.print(f"[green]✓ Github fallback fetch successful for {doc_id}[/green]")
                    else:
                        console.print(f"[yellow]⚠ Github fallback failed: Invalid doc_id format {doc_id}[/yellow]")
                except Exception as e:
                    console.print(f"[yellow]⚠ Warning: Github fallback fetch failed for {doc_id}: {e}[/yellow]")

    if not shutil.which("ruff"):
        console.print("[red]Error: ruff is not installed. Run `pip install ruff`[/red]")
        sys.exit(1)

    cmd = ["ruff", "check", "--select", "UP", "--output-format", "json"] + [str(f) for f in py_files]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    
    try:
        ruff_output = json.loads(res.stdout) if res.stdout.strip() else []
    except json.JSONDecodeError:
        console.print(f"[red]Error: Failed to parse ruff output: {res.stdout}[/red]")
        sys.exit(1)

    import re
    
    def get_dynamic_deprecations(doc_path: Path) -> list[str]:
        if not doc_path.exists():
            return []
        content = doc_path.read_text(encoding="utf-8", errors="replace")
        bad_patterns = []
        for line in content.splitlines():
            line_lower = line.lower()
            if any(kw in line_lower for kw in ["incorrect", "deprecated", "legacy", "do not use", "avoid"]):
                matches = re.findall(r'`([^`]+)`', line)
                for m in matches:
                    clean_m = m.replace("...", "").strip()
                    if clean_m.endswith("()"):
                        clean_m = clean_m[:-2]
                    if clean_m.endswith("("):
                        clean_m = clean_m[:-1]
                    if clean_m and len(clean_m) > 4 and (" " in clean_m or "." in clean_m):
                        if clean_m.startswith("import ") and " as " in clean_m:
                            clean_m = clean_m.split(" as ")[0].strip()
                        bad_patterns.append(clean_m)
        return list(set(bad_patterns))

    dynamic_patterns = {}
    for doc_id in all_needed_docs:
        safe_name = doc_id.replace("/", "__")
        doc_path = DOCS_DIR / f"{safe_name}.md"
        dynamic_patterns[doc_id] = get_dynamic_deprecations(doc_path)

    # Synthesize UP035 violations for known deprecated AI SDK patterns
    for f in py_files:
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(content)
            lines = content.splitlines()
        except Exception:
            continue

        def add_synth(line, col, mod, msg):
            if line - 1 < len(lines) and "# noqa: UP" in lines[line - 1]:
                return
            # Prevent duplicates
            if not any(v["location"]["row"] == line and v.get("_synth_mod") == mod for v in ruff_output):
                ruff_output.append({
                    "filename": str(f),
                    "location": {"row": line, "column": col},
                    "code": "UP035",
                    "message": msg,
                    "_synth_mod": mod
                })

        # Step 1: Highly precise AST fallback for the most critical framework breakages
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "google.generativeai":
                        add_synth(node.lineno, node.col_offset + 1, "google.generativeai", "`import google.generativeai` is deprecated") # noqa: UP035
            elif isinstance(node, ast.ImportFrom):
                if node.module == "google.generativeai":
                    add_synth(node.lineno, node.col_offset + 1, "google.generativeai", f"`from {node.module} ...` is deprecated") # noqa: UP035
                elif node.module == "langchain.chat_models" and any(a.name == "ChatOpenAI" for a in node.names):
                    add_synth(node.lineno, node.col_offset + 1, "langchain", "`from langchain.chat_models import ChatOpenAI` is deprecated. Use `langchain_openai`.") # noqa: UP035
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute) and node.func.attr == "create":
                    if isinstance(node.func.value, ast.Attribute) and node.func.value.attr == "ChatCompletion":
                        if isinstance(node.func.value.value, ast.Name) and node.func.value.value.id == "openai":
                            add_synth(node.lineno, node.col_offset + 1, "openai", "`openai.ChatCompletion.create()` is deprecated") # noqa: UP035
                    elif isinstance(node.func.value, ast.Attribute) and node.func.value.attr == "completions":
                        if isinstance(node.func.value.value, ast.Attribute) and node.func.value.value.attr == "chat":
                            add_synth(node.lineno, node.col_offset + 1, "openai", "`client.chat.completions.create(...)` is deprecated. See modern responses API.") # noqa: UP035
                        elif isinstance(node.func.value.value, ast.Call):
                            # anthropic.Anthropic().completions.create
                            if isinstance(node.func.value.value.func, ast.Attribute) and node.func.value.value.func.attr == "Anthropic":
                                add_synth(node.lineno, node.col_offset + 1, "anthropic", "Legacy text completions API `Anthropic().completions.create()` is deprecated. Use Messages API.") # noqa: UP035

        # Step 2: Dynamic text matching against chub guidelines (for explicit string matches)
        for line_idx, line in enumerate(lines):
            if "# noqa: UP" in line:
                continue
            
            for doc_id, patterns in dynamic_patterns.items():
                for pattern in patterns:
                    if pattern in line:
                        mod_key = next((k for k, v in registry.items() if v == doc_id), doc_id.split("/")[0])
                        add_synth(line_idx + 1, line.find(pattern) + 1, mod_key, f"`{pattern}` is flagged as deprecated or incorrect by chub docs.")

    violations = []
    for item in ruff_output:
        code = item.get("code", "")
        if not code.startswith("UP"):
            continue
            
        file_path = Path(item["filename"])
        
        doc_id_for_file = None
        hint = None
        
        # Prioritize synthesized mod for hint matching, fallback to file-level modules
        synth_mod = item.get("_synth_mod")
        
        # Only attach hints to synthesized violations or if it's explicitly an SDK violation
        # to avoid polluting standard Python pyupgrade warnings with AI SDK docs.
        if synth_mod and synth_mod in registry:
            doc_id_for_file = registry[synth_mod]
            safe_name = doc_id_for_file.replace("/", "__")
            doc_path = DOCS_DIR / f"{safe_name}.md"
            hint = extract_chub_hint(doc_path)
        elif not synth_mod:
            # If it's a regular ruff UP warning, just report it without attaching AI hints
            # to prevent confusing standard library deprecations with SDK docs.
            pass

        # Robust nested path resolution: resolve both to absolute, then compute relative
        try:
            display_name = file_path.resolve().relative_to(REPO_ROOT.resolve())
        except ValueError:
            display_name = file_path

        v = Violation(
            filename=display_name,
            line=item["location"]["row"],
            col=item["location"]["column"],
            code=code,
            message=item.get("message", "Deprecated usage detected"),
            chub_hint=hint,
            doc_id=doc_id_for_file
        )
        violations.append(v)

    if not violations:
        console.print("[green]✓ No deprecated API calls detected[/green]")
        sys.exit(0)

    # ── Summary header ──────────────────────────────────────────────
    console.print()
    console.print(Rule("[bold red]DEPRECATED API USAGE DETECTED[/bold red]", style="red"))
    console.print()

    # Count violations per file for the header
    file_counts = {}
    for v in violations:
        fname = str(v.filename)
        file_counts[fname] = file_counts.get(fname, 0) + 1

    summary_text = Text()
    summary_text.append(f"  Found ", style="bold")
    summary_text.append(f"{len(violations)}", style="bold red")
    summary_text.append(f" issue{'s' if len(violations) != 1 else ''} across ", style="bold")
    summary_text.append(f"{len(file_counts)}", style="bold red")
    summary_text.append(f" file{'s' if len(file_counts) != 1 else ''}\n", style="bold")
    console.print(summary_text)

    # ── Violations table ────────────────────────────────────────────
    table = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
        title_style="bold",
        pad_edge=True,
        expand=True,
    )
    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("File", style="yellow", no_wrap=True, ratio=3)
    table.add_column("Line", style="magenta", width=6, justify="right")
    table.add_column("Code", style="cyan", width=7)
    table.add_column("Issue", ratio=6)

    seen_hints = {}  # doc_id → chub_hint (deduplicate)
    for idx, v in enumerate(violations, 1):
        # Build the issue text with color
        issue = Text(v.message)
        if v.doc_id:
            issue.append(f"  [{v.doc_id}]", style="dim")

        table.add_row(
            str(idx),
            str(v.filename),
            str(v.line),
            v.code,
            issue,
        )

        # Collect unique hints
        if v.chub_hint and v.doc_id and v.doc_id not in seen_hints:
            seen_hints[v.doc_id] = v.chub_hint

    console.print(table)

    # ── Chub hints (one per SDK) ────────────────────────────────────
    if seen_hints:
        console.print()
        console.print(Rule("[bold green]RECOMMENDED FIXES[/bold green]", style="green"))
        console.print()
        for doc_id, hint_code in seen_hints.items():
            hint_panel = Syntax(hint_code, "python", theme="monokai", line_numbers=False, word_wrap=True)
            console.print(Panel(
                hint_panel,
                title=f"[bold green]✦ {doc_id}[/bold green]",
                subtitle=f"[dim]chub get {doc_id} --lang python[/dim]",
                border_style="green",
                padding=(1, 2),
            ))

    # ── Footer ──────────────────────────────────────────────────────
    console.print()
    console.print(Panel(
        "[bold]Commit blocked.[/bold] Fix the issues listed above and re-commit.\n"
        "[dim]To suppress a false positive, add[/dim]  [cyan]# noqa: UP<code>[/cyan]  [dim]to the line.[/dim]",
        border_style="red",
        padding=(0, 2),
    ))
    console.print()

    # ── Generate markdown report (append to history) ──────────────────
    report_path = REPO_ROOT / "chub_guard_report.md"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Build this run's section
    run_lines = [
        f"## 🕐 Run: {timestamp}",
        "",
        f"**{len(violations)}** issue{'s' if len(violations) != 1 else ''} found across **{len(file_counts)}** file{'s' if len(file_counts) != 1 else ''}.",
        "",
        "### Issues",
        "",
        "| # | File | Line | Code | Issue |",
        "|---|------|------|------|-------|",
    ]
    for idx, v in enumerate(violations, 1):
        issue_text = v.message
        if v.doc_id:
            issue_text += f" *[{v.doc_id}]*"
        issue_text = issue_text.replace("|", "\\|")
        fname = str(v.filename).replace("\\", "/")
        run_lines.append(f"| {idx} | `{fname}` | {v.line} | `{v.code}` | {issue_text} |")

    if seen_hints:
        run_lines += [
            "",
            "### Recommended Fixes",
        ]
        for doc_id, hint_code in seen_hints.items():
            run_lines += [
                "",
                f"#### ✦ `{doc_id}`",
                "",
                "```python",
                hint_code,
                "```",
                "",
                f"> Full docs: `chub get {doc_id} --lang python`",
            ]

    run_lines += [
        "",
        "*To suppress a false positive, add `# noqa: UP<code>` to the line.*",
        "",
        "---",
        "",
    ]

    run_section = "\n".join(run_lines)

    # Read existing report — extract previous run summary for compact history log
    REPORT_TITLE = "# 🛡️ Chub Guard Report\n\n"
    HISTORY_HEADER = "## Previous Runs\n\n"
    try:
        past_entries = []
        if report_path.exists():
            existing = report_path.read_text(encoding="utf-8")
            # Extract the previous "latest" run's timestamp + summary as a one-liner
            import re
            prev_run = re.search(r"## 🕐 Run: (.+)\n\n\*\*(\d+)\*\* issue.*?across \*\*(\d+)\*\* file", existing)
            if prev_run:
                past_entries.append(f"- `{prev_run.group(1)}` — {prev_run.group(2)} issue(s) across {prev_run.group(3)} file(s)")
            # Carry forward any existing history entries
            history_match = re.search(r"## Previous Runs\n\n((?:- .+\n)*)", existing)
            if history_match:
                past_entries.extend(history_match.group(1).strip().splitlines())

        # Build the full report: title + latest run details + compact history
        full_report = REPORT_TITLE + run_section
        if past_entries:
            full_report += HISTORY_HEADER + "\n".join(past_entries) + "\n"

        report_path.write_text(full_report, encoding="utf-8")
        console.print(f"[dim]📄 Report updated → {report_path.relative_to(REPO_ROOT)}[/dim]")
    except Exception as e:
        console.print(f"[yellow]⚠ Could not write report: {e}[/yellow]")

    sys.exit(1)


@cli.command()
def update_registry():
    """Searches chub registry for new AI/ML SDK entries."""
    chub_cmd = shutil.which("chub")
    if not chub_cmd:
        console.print("[red]Error: chub is not installed.[/red]")
        sys.exit(1)

    try:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        console.print(f"[red]Error loading registry: {e}[/red]")
        sys.exit(1)

    new_entries = {}
    
    for tag in ["ai", "ml"]:
        try:
            res = subprocess.run([chub_cmd, "search", tag, "--json"], capture_output=True, text=True, timeout=30)
            if res.returncode == 0 and res.stdout.strip():
                data = json.loads(res.stdout)
                results_list = data.get("results", []) if isinstance(data, dict) else data
                for item in results_list:
                    # simplistic heuristic: if we can guess the python import name
                    doc_id = item.get("id")
                    if doc_id:
                        pkg = doc_id.split("/")[-1]
                        if pkg not in registry.values() and pkg not in registry:
                            new_entries[pkg] = doc_id
        except Exception as e:
            console.print(f"[yellow]⚠ Failed to search chub for {tag}: {e}[/yellow]")
            
    if not new_entries:
        console.print("[green]Registry is up to date.[/green]")
        return
        
    console.print("[cyan]Proposed Additions:[/cyan]")
    for k, v in new_entries.items():
        console.print(f"  \"{k}\": \"{v}\"")
        
    if click.confirm("Add these to registry.json?"):
        registry.update(new_entries)
        REGISTRY_PATH.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
        console.print("[green]✓ Registry updated.[/green]")


if __name__ == "__main__":
    cli()
