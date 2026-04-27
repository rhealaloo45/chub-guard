import ast
import os
import re
import datetime
import json
import shutil
import subprocess
import sys
import time
import urllib.request
import urllib.error
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Dict, Set, Tuple

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

# Path Resolution
REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / ".chub-docs"
REGISTRY_PATH = DOCS_DIR / "registry.json"

NON_PY_EXTENSIONS = {".js", ".ts", ".jsx", ".tsx", ".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx", ".java"}
JS_TS_EXTENSIONS = {".js", ".ts", ".jsx", ".tsx"}
C_EXTENSIONS = {".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx"}
JAVA_EXTENSIONS = {".java"}

STDLIB_MODS = {"os", "sys", "re", "json", "ast", "time", "math", "pathlib", "typing", "datetime", "collections",
               "functools", "itertools", "subprocess", "shutil", "urllib", "http", "io", "abc", "copy", "enum",
               "dataclasses", "contextlib", "logging", "warnings", "threading", "multiprocessing", "socket", "hashlib",
               "base64", "struct", "random", "string", "textwrap", "unittest", "pytest", "argparse", "pdb", "glob"}

CHUB_GLOBAL_REGISTRY = Path.home() / ".chub" / "sources" / "default" / "registry.json"
HISTORICAL_DB_DIR = Path.home() / ".chub" / "cache"
HISTORICAL_DB_PATH = HISTORICAL_DB_DIR / "historical_deprecations.json"
HISTORICAL_DB_URL = "https://raw.githubusercontent.com/rhealaloo45/chub-guard/main/deprecations.json"

@dataclass
class Violation:
    filename: Path
    line: int
    col: int
    code: str
    message: str
    chub_hint: Optional[str] = None
    doc_id: Optional[str] = None

def _load_global_chub_registry() -> Tuple[Dict[str, str], Dict[str, List[str]]]:
    if not CHUB_GLOBAL_REGISTRY.exists(): return {}, {}
    try:
        data = json.loads(CHUB_GLOBAL_REGISTRY.read_text(encoding="utf-8"))
        lookup, doc_langs = {}, {}
        for doc in data.get("docs", []):
            doc_id = doc.get("id", "")
            if not doc_id: continue
            doc_langs[doc_id] = [l.get("language") for l in doc.get("languages", []) if l.get("language")]
            base = doc_id.split("/")[0]
            sub = doc_id.split("/")[1] if "/" in doc_id else ""
            lookup[base] = doc_id
            if sub: lookup[f"{base}/{sub}"] = doc_id
        return lookup, doc_langs
    except Exception: return {}, {}

def get_imported_modules(file_path: Path) -> Dict[str, List[Tuple[int, int]]]:
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(content)
        modules = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names: modules[n.name.split(".")[0]] = modules.get(n.name.split(".")[0], []) + [(node.lineno, node.col_offset + 1)]
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules[node.module.split(".")[0]] = modules.get(node.module.split(".")[0], []) + [(node.lineno, node.col_offset + 1)]
        return modules
    except Exception: return {}

def get_js_imports(file_path: Path) -> Dict[str, List[Tuple[int, int]]]:
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
        modules = {}
        for i, line in enumerate(content.splitlines()):
            m = re.search(r"""from\s+['"]([^'"]+)['"]""", line) or re.search(r"""require\s*\(\s*['"]([^'"]+)['"]\s*\)""", line)
            if m:
                pkg = m.group(1).split("/")[0]
                modules[pkg] = modules.get(pkg, []) + [(i+1, line.find(pkg)+1)]
        return modules
    except Exception: return {}

def get_dynamic_deprecations(doc_path: Path) -> List[str]:
    if not doc_path.exists(): return []
    def _extract(p: Path):
        content = p.read_text(encoding="utf-8", errors="replace")
        bad = []
        neg = ["incorrect", "deprecated", "legacy", "do not use", "removed", "❌", "instead", "copy", "warn", "pitfall"]
        for line in content.splitlines():
            lower = line.lower()
            if any(k in lower for k in neg) and not ("instead" in lower and "`" not in line[:lower.find("instead")]):
                matches = re.findall(r'`([^`]+)`', line)
                for m in matches:
                    if len(m) > 3: bad.append(m.strip("()").strip())
        return bad
    patterns = _extract(doc_path)
    full = doc_path.parent / doc_path.name.replace(".md", "__full.md")
    if full.exists(): patterns.extend(_extract(full))
    return list(set(patterns))

def extract_chub_hint(doc_path: Path, lang: str = "python") -> Optional[str]:
    if not doc_path.exists(): return None
    content = doc_path.read_text(encoding="utf-8", errors="replace")
    fence = f"```{lang}" if lang != "python" else "```python"
    code_lines = []
    in_block = False
    for line in content.splitlines():
        if line.strip().startswith(fence): in_block = True; continue
        if line.strip().startswith("```") and in_block: break
        if in_block: code_lines.append(line)
    return "\n".join(code_lines) if code_lines else None

class PythonAdvancedAnalyzer(ast.NodeVisitor):
    def __init__(self, filename, content, registry):
        self.filename, self.content, self.registry = filename, content, registry
        self.violations = []
    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == "ClientSession":
            self.violations.append(Violation(self.filename, node.lineno, node.col_offset+1, "CHUB", "aiohttp.ClientSession() should be used with `async with`.", doc_id="aiohttp"))
        self.generic_visit(node)

def analyze_js_file(f: Path, registry: dict, dynamic_patterns: dict) -> List[Violation]:
    violations = []
    imports = get_js_imports(f)
    try:
        content = f.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
        for mod, locs in imports.items():
            doc_id = registry.get(mod)
            if doc_id and doc_id in dynamic_patterns:
                for pattern in dynamic_patterns[doc_id]:
                    for i, line in enumerate(lines):
                        if pattern in line and "// noqa" not in line:
                            violations.append(Violation(f, i+1, line.find(pattern)+1, "CHUB", f"`{pattern}` is deprecated according to chub docs.", doc_id=doc_id))
    except Exception: pass
    return violations

def _sync_global_db():
    if not HISTORICAL_DB_DIR.exists(): HISTORICAL_DB_DIR.mkdir(parents=True, exist_ok=True)
    if HISTORICAL_DB_PATH.exists() and (time.time() - HISTORICAL_DB_PATH.stat().st_mtime) < 86400: return
    try:
        req = urllib.request.Request(HISTORICAL_DB_URL, headers={'User-Agent': 'chub-guard/1.2.1'})
        with urllib.request.urlopen(req, timeout=5) as r:
            HISTORICAL_DB_PATH.write_text(r.read().decode("utf-8"), encoding="utf-8")
    except Exception: pass

def _load_historical_db() -> Dict[str, List[str]]:
    if not HISTORICAL_DB_PATH.exists(): return {}
    try:
        data = json.loads(HISTORICAL_DB_PATH.read_text(encoding="utf-8"))
        patterns = {}
        for doc_id, entry in data.items():
            patterns[doc_id] = entry.get("patterns", [])
        return patterns
    except Exception: return {}

def generate_markdown_report(violations: List[Violation], project_root: Path):
    report_path = (project_root if project_root else REPO_ROOT) / "chub_guard_report.md"
    content = ["# 🛡️ Chub Guard Security & Deprecation Report", f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"]
    content.append(f"## Summary: {len(violations)} issues found\n")
    for v in violations:
        content.append(f"### 🚩 {v.message}")
        content.append(f"- **File:** `{v.filename}` (Line {v.line})")
        if v.chub_hint: content.append(f"\n**Recommended Fix:**\n```python\n{v.chub_hint}\n```")
        content.append("\n---\n")
    report_path.write_text("\n".join(content), encoding="utf-8")

@click.group()
def cli(): pass

@cli.command()
@click.argument("filenames", nargs=-1, type=click.Path(exists=True, path_type=Path))
@click.option("--json", "as_json", is_flag=True)
@click.option("--root", "project_root", type=click.Path(exists=True, path_type=Path))
def scan(filenames, as_json, project_root):
    _sync_global_db()
    scan_root = (project_root if project_root else REPO_ROOT).resolve()
    files_to_scan = []
    if filenames:
        files_to_scan = list(filenames)
    else:
        ignored = {".git", "node_modules", "venv", ".venv", "__pycache__", "dist", "build"}
        for root, dirs, files in os.walk(scan_root):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ignored]
            for f in files:
                if any(f.endswith(ext) for ext in [".py"] + list(NON_PY_EXTENSIONS)):
                    files_to_scan.append(Path(root) / f)

    try:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except Exception: registry = {}

    py_files = [f for f in files_to_scan if f.suffix == ".py"]
    js_files = [f for f in files_to_scan if f.suffix in JS_TS_EXTENSIONS]
    
    all_needed = set()
    for f in py_files:
        for mod in get_imported_modules(f):
            if mod in registry: all_needed.add(registry[mod])
    for f in js_files:
        for mod in get_js_imports(f):
            if mod in registry: all_needed.add(registry[mod])

    dynamic_patterns = {doc_id: get_dynamic_deprecations(DOCS_DIR / f"{doc_id.replace('/', '__')}.md") for doc_id in all_needed}
    historical_patterns = _load_historical_db()

    violations = []

    # Batch Ruff check (much faster)
    if py_files and shutil.which("ruff"):
        try:
            # Run ruff on all py_files at once
            res = subprocess.run(["ruff", "check", "--select", "UP", "--output-format", "json"] + [str(f) for f in py_files], capture_output=True, text=True)
            if res.stdout:
                for item in json.loads(res.stdout):
                    violations.append(Violation(Path(item["filename"]), item["location"]["row"], item["location"]["column"], item["code"], item["message"]))
        except Exception: pass

    # Python Analysis
    for f in py_files:
        # AST & Dynamic check
        content = f.read_text(encoding="utf-8", errors="replace")
        analyzer = PythonAdvancedAnalyzer(f, content, registry)
        try: analyzer.visit(ast.parse(content))
        except Exception: pass
        violations.extend(analyzer.violations)
        
        lines = content.splitlines()
        for i, line in enumerate(lines):
            # Check dynamic patterns from docs
            for doc_id, patterns in dynamic_patterns.items():
                for p in patterns:
                    if p in line and "# noqa" not in line:
                        violations.append(Violation(f, i+1, line.find(p)+1, "CHUB", f"`{p}` is deprecated.", doc_id=doc_id))
            
            # Check historical patterns from global DB
            for doc_id, patterns in historical_patterns.items():
                for p in patterns:
                    if p in line and "# noqa" not in line:
                        # Only add if not already found (avoid duplicates)
                        exists = any(v.filename == f and v.line == i+1 and p in v.message for v in violations)
                        if not exists:
                            violations.append(Violation(f, i+1, line.find(p)+1, "CHUB", f"`{p}` is known to be deprecated/legacy.", doc_id=doc_id))

    # JS Analysis
    for f in js_files:
        violations.extend(analyze_js_file(f, registry, dynamic_patterns))
        # Also check historical for JS
        content = f.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
        for i, line in enumerate(lines):
            for doc_id, patterns in historical_patterns.items():
                for p in patterns:
                    if p in line and "// noqa" not in line:
                        exists = any(v.filename == f and v.line == i+1 and p in v.message for v in violations)
                        if not exists:
                            violations.append(Violation(f, i+1, line.find(p)+1, "CHUB", f"`{p}` is known to be deprecated/legacy.", doc_id=doc_id))

    # Normalize paths for display
    for v in violations:
        try: v.filename = v.filename.resolve().relative_to(scan_root)
        except Exception: pass
        if v.doc_id:
            v.chub_hint = extract_chub_hint(DOCS_DIR / f"{v.doc_id.replace('/', '__')}.md")

    if as_json:
        results = [{"filename": str(v.filename), "location": {"row": v.line, "column": v.col}, "code": v.code, "message": v.message, "chub_hint": v.chub_hint, "doc_id": v.doc_id} for v in violations]
        print(json.dumps(results))
        generate_markdown_report(violations, project_root)
        sys.exit(0 if not violations else 1)
    
    # CLI Output
    if not violations:
        console.print("[green]✓ Clean scan![/green]")
    else:
        console.print(f"[bold red]Found {len(violations)} issues![/bold red]")
        for v in violations:
            console.print(f"  {v.filename}:{v.line} - {v.message}")
        generate_markdown_report(violations, project_root)

if __name__ == "__main__":
    cli()
