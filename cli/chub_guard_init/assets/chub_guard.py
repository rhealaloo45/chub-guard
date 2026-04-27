import ast
import os
import re
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

NON_PY_EXTENSIONS = {".js", ".ts", ".jsx", ".tsx", ".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx", ".java"}
JS_TS_EXTENSIONS = {".js", ".ts", ".jsx", ".tsx"}
C_EXTENSIONS = {".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx"}
JAVA_EXTENSIONS = {".java"}

STDLIB_MODS = {"os", "sys", "re", "json", "ast", "time", "math",
               "pathlib", "typing", "datetime", "collections",
               "functools", "itertools", "subprocess", "shutil",
               "urllib", "http", "io", "abc", "copy", "enum",
               "dataclasses", "contextlib", "logging", "warnings",
               "threading", "multiprocessing", "socket", "hashlib",
               "base64", "struct", "random", "string", "textwrap",
               "unittest", "pytest", "argparse", "pdb", "glob",
               "csv", "pickle", "pprint", "tempfile", "traceback",
               "inspect", "operator", "heapq", "bisect", "array",
               "queue", "signal", "select", "ssl", "email",
               "html", "xml", "sqlite3", "decimal", "fractions",
               "asyncio", "concurrent", "typing_extensions", "__future__",
               "builtins", "gc", "weakref", "types", "dis", "cProfile",
               "profile", "timeit", "atexit", "sysconfig", "platform",
               "ctypes", "mmap", "readline", "rlcompleter"}

# Global chub registry installed at ~/.chub/sources/default/registry.json
CHUB_GLOBAL_REGISTRY = Path.home() / ".chub" / "sources" / "default" / "registry.json"

# GAP 6: Historical deprecations database paths
HISTORICAL_DB_PATH = DOCS_DIR / "historical_deprecations.json"
HISTORICAL_DB_URL = "https://raw.githubusercontent.com/rhealaloo45/chub-guard/main/deprecations.json"


def _load_global_chub_registry() -> tuple[dict[str, str], dict[str, list[str]]]:
    """Load the global chub registry and build lookups.
    
    Returns:
        tuple: (module_name → doc_id, doc_id → [languages])
    """
    if not CHUB_GLOBAL_REGISTRY.exists():
        return {}, {}
    try:
        data = json.loads(CHUB_GLOBAL_REGISTRY.read_text(encoding="utf-8"))
        docs = data.get("docs", [])
        lookup = {}
        doc_langs = {}
        for doc in docs:
            doc_id = doc.get("id", "")
            if not doc_id:
                continue
            
            # Extract supported languages
            langs = [l.get("language") for l in doc.get("languages", []) if l.get("language")]
            doc_langs[doc_id] = langs

            parts = doc_id.split("/")
            base = parts[0]  # e.g. "openai", "langchain"
            sub = parts[1] if len(parts) > 1 else ""  # e.g. "package", "core"
            
            if base not in lookup:
                lookup[base] = doc_id
            if sub == "package":
                lookup[base] = doc_id
            if sub and sub != "package":
                lookup[f"{base}-{sub}"] = doc_id
                lookup[f"{base}_{sub}"] = doc_id
                lookup[f"{base}/{sub}"] = doc_id  # Added slash for better resolution

        return lookup, doc_langs
    except Exception:
        return {}, {}


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
        if line - 1 < len(lines) and any(kw in lines[line - 1] for kw in ["# noqa: UP", "# noqa: CHUB"]):
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


def get_js_imports(file_path: Path) -> dict[str, list[tuple[int, int]]]:
    """Extract imports from JS/TS files using regex."""
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        console.print(f"[yellow]⚠ Warning: Error reading {file_path}: {e}. Skipping.[/yellow]")
        return {}

    modules = {}
    lines = content.splitlines()

    for line_idx, line in enumerate(lines):
        # Check for noqa suppression
        if "// noqa: CHUB" in line or "# noqa: CHUB" in line:
            continue

        pkg = None

        # import X from 'pkg' or import X, { Y } from "pkg"
        m = re.match(r"""import\s+(?:[^'"]+)\s+from\s+['"]([^'"]+)['"]""", line.strip())
        if m:
            pkg = m.group(1)

        # require('pkg') or require("pkg")
        if not pkg:
            m = re.search(r"""require\s*\(\s*['"]([^'"]+)['"]\s*\)""", line)
            if m:
                pkg = m.group(1)

        # C/C++: #include <pkg/header> or #include "pkg/header"
        if not pkg:
            m = re.match(r"""#include\s*[<"]([^>"]+)[>"]""", line.strip())
            if m:
                # e.g., curl/curl.h -> try "curl/curl.h"
                pkg = m.group(1).replace('.h', '').replace('.hpp', '')

        # Java: import java.util.List;
        if not pkg:
            m = re.match(r"""import\s+(static\s+)?([a-zA-Z0-9_.]+);""", line.strip())
            if m:
                # Convert dot notation to slash notation for chub registry lookup
                pkg = m.group(2).replace('.', '/')

        if pkg:
            if pkg not in modules:
                modules[pkg] = []
            modules[pkg].append((line_idx + 1, line.find(pkg) + 1))

            # Also add the top-level package name for registry lookup
            if pkg.startswith("@"):
                # @anthropic-ai/sdk -> try anthropic-ai/sdk then anthropic
                stripped = pkg[1:]  # anthropic-ai/sdk
                parts = stripped.split("/")
                top_level = parts[0] if parts else stripped  # anthropic-ai
                simple = top_level.split("-")[0]  # anthropic
                for alias in [stripped, top_level, simple]:
                    if alias and alias != pkg:
                        if alias not in modules:
                            modules[alias] = []
                        modules[alias].append((line_idx + 1, line.find(pkg) + 1))
            else:
                top_level = pkg.split("/")[0]
                if top_level != pkg:
                    if top_level not in modules:
                        modules[top_level] = []
                    modules[top_level].append((line_idx + 1, line.find(pkg) + 1))

    return modules


# ── GAP 1: Polarity-aware pattern extraction helper ─────────────────

def _extract_from_doc(doc_path: Path) -> list[str]:
    """Core pattern-extraction logic used by both main doc and __full doc."""
    if not doc_path.exists():
        return []
    content = doc_path.read_text(encoding="utf-8", errors="replace")
    bad_patterns = []

    NEGATIVE_KWS = ["incorrect", "deprecated", "legacy", "do not use",
                    "do not", "avoid", "prohibited", "removed", "old way",
                    "don't use", "❌", "⛔", "🚫"]
    POSITIVE_KWS  = ["instead", "use this", "correct", "modern", "new way",
                     "recommended", "✅", "do this", "replacement"]
    SPLIT_MARKERS = ["→", "->", " instead", " use ", "replace with",
                     "✅", "correct:", "modern:"]

    for line in content.splitlines():
        line_lower = line.lower()

        # Skip lines that are purely positive
        if any(kw in line_lower for kw in POSITIVE_KWS) and not any(kw in line_lower for kw in NEGATIVE_KWS):
            continue

        if not any(kw in line_lower for kw in NEGATIVE_KWS):
            continue

        # Split on arrow/replacement markers — only take the LEFT side
        working = line
        for marker in SPLIT_MARKERS:
            if marker.lower() in working.lower():
                idx = working.lower().find(marker.lower())
                working = working[:idx]
                break

        matches = re.findall(r'`([^`]+)`', working)
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

    # Strategy 2: Scan deprecated/legacy SECTION headers
    # Find ## Deprecated, ## Legacy, ## Removal sections and extract ALL
    # backtick patterns within them regardless of per-line keywords
    in_deprecated_section = False
    for line in content.splitlines():
        stripped = line.strip().lower()
        if stripped.startswith("## "):
            in_deprecated_section = any(
                kw in stripped for kw in
                ["deprecated", "legacy", "removal", "removed", "breaking", "migration"]
            )
            continue
        if in_deprecated_section:
            for m in re.findall(r'`([^`]+)`', line):
                clean_m = m.replace("...", "").strip()
                if clean_m.endswith("()"):
                    clean_m = clean_m[:-2]
                if clean_m.endswith("("):
                    clean_m = clean_m[:-1]
                if clean_m and len(clean_m) > 3:
                    bad_patterns.append(clean_m)

    # Strategy 3: Explicit ❌ code blocks
    # Find fenced code blocks immediately preceded by ❌/⛔/🚫 within 3 lines
    lines_list = content.splitlines()
    i = 0
    while i < len(lines_list):
        line = lines_list[i]
        if any(marker in line for marker in ["❌", "⛔", "🚫", "**Don't", "**Incorrect", "**Deprecated"]):
            # Look ahead for a code block within 3 lines
            for j in range(i + 1, min(i + 4, len(lines_list))):
                if lines_list[j].strip().startswith("```"):
                    # Check no positive marker appears between i and j
                    between = " ".join(lines_list[i:j]).lower()
                    if not any(pk in between for pk in ["✅", "**do ", "**correct", "**modern"]):
                        # Extract all identifiers from this code block
                        k = j + 1
                        while k < len(lines_list) and not lines_list[k].strip().startswith("```"):
                            for m in re.findall(r'`([^`]+)`|(\b[A-Z][a-zA-Z]+(?:\.[a-zA-Z]+)+)', lines_list[k]):
                                pattern = m[0] or m[1]
                                if pattern and len(pattern) > 3:
                                    bad_patterns.append(pattern.strip("()"))
                            k += 1
                    break
        i += 1

    return list(set(bad_patterns))


def get_dynamic_deprecations(doc_path: Path) -> list[str]:
    """Extract deprecated patterns from chub docs with polarity-aware parsing."""
    if not doc_path.exists():
        return []
    bad_patterns = _extract_from_doc(doc_path)

    # Also extract from full reference doc if available (GAP 5)
    full_path = doc_path.parent / doc_path.name.replace(".md", "__full.md")
    if full_path.exists() and full_path.is_file():
        bad_patterns.extend(_extract_from_doc(full_path))

    return list(set(bad_patterns))


def get_js_dynamic_deprecations(doc_path: Path) -> list[str]:
    """Extract deprecated patterns from JS chub docs with polarity-aware parsing."""
    if not doc_path.exists():
        return []
    content = doc_path.read_text(encoding="utf-8", errors="replace")
    bad_patterns = []

    NEGATIVE_KWS = ["incorrect", "deprecated", "legacy", "do not use",
                    "do not", "avoid", "prohibited", "removed", "old way",
                    "don't use", "❌", "⛔", "🚫"]
    POSITIVE_KWS  = ["instead", "use this", "correct", "modern", "new way",
                     "recommended", "✅", "do this", "replacement"]
    SPLIT_MARKERS = ["→", "->", " instead", " use ", "replace with",
                     "✅", "correct:", "modern:"]

    for line in content.splitlines():
        line_lower = line.lower()

        # Skip lines that are purely positive
        if any(kw in line_lower for kw in POSITIVE_KWS) and not any(kw in line_lower for kw in NEGATIVE_KWS):
            continue

        if not any(kw in line_lower for kw in NEGATIVE_KWS):
            continue

        # Split on arrow/replacement markers — only take the LEFT side
        working = line
        for marker in SPLIT_MARKERS:
            if marker.lower() in working.lower():
                idx = working.lower().find(marker.lower())
                working = working[:idx]
                break

        matches = re.findall(r'`([^`]+)`', working)
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

        # JS-specific pattern extraction (kept from original)
        for m in re.findall(r'new\s+(\w+)\s*\(', working):
            if len(m) > 3:
                bad_patterns.append(f"new {m}(")
        for m in re.findall(r'(\w+(?:\.\w+)+)\s*\(', working):
            if len(m) > 4:
                bad_patterns.append(m)
        for m in re.findall(r"""require\s*\(\s*['"]([^'"]+)['"]\s*\)""", working):
            if len(m) > 3:
                bad_patterns.append(f"require('{m}')")

    # Strategy 2: Scan deprecated/legacy SECTION headers
    in_deprecated_section = False
    for line in content.splitlines():
        stripped = line.strip().lower()
        if stripped.startswith("## "):
            in_deprecated_section = any(
                kw in stripped for kw in
                ["deprecated", "legacy", "removal", "removed", "breaking", "migration"]
            )
            continue
        if in_deprecated_section:
            for m in re.findall(r'`([^`]+)`', line):
                clean_m = m.replace("...", "").strip()
                if clean_m.endswith("()"):
                    clean_m = clean_m[:-2]
                if clean_m.endswith("("):
                    clean_m = clean_m[:-1]
                if clean_m and len(clean_m) > 3:
                    bad_patterns.append(clean_m)

    # Strategy 3: Explicit ❌ code blocks
    lines_list = content.splitlines()
    i = 0
    while i < len(lines_list):
        line = lines_list[i]
        if any(marker in line for marker in ["❌", "⛔", "🚫", "**Don't", "**Incorrect", "**Deprecated"]):
            for j in range(i + 1, min(i + 4, len(lines_list))):
                if lines_list[j].strip().startswith("```"):
                    between = " ".join(lines_list[i:j]).lower()
                    if not any(pk in between for pk in ["✅", "**do ", "**correct", "**modern"]):
                        k = j + 1
                        while k < len(lines_list) and not lines_list[k].strip().startswith("```"):
                            for m in re.findall(r'`([^`]+)`|(\b[A-Z][a-zA-Z]+(?:\.[a-zA-Z]+)+)', lines_list[k]):
                                pattern = m[0] or m[1]
                                if pattern and len(pattern) > 3:
                                    bad_patterns.append(pattern.strip("()"))
                            k += 1
                    break
        i += 1

    # Also extract from full reference doc if available (GAP 5)
    full_path = doc_path.parent / doc_path.name.replace(".md", "__full.md")
    if full_path.exists() and full_path.is_file():
        bad_patterns.extend(_extract_from_doc(full_path))

    return list(set(bad_patterns))


def analyze_js_file(f: Path, registry: dict, dynamic_patterns: dict) -> list[dict]:
    """Run regex-based deprecation detection on a JS/TS file."""
    try:
        content = f.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
    except Exception:
        return []

    violations = []
    js_imports = get_js_imports(f)

    # Find which doc_ids are relevant for this file
    relevant_doc_ids = set()
    
    # 1. Dynamic patterns from chub docs
    for mod in js_imports:
        if mod in registry:
            relevant_doc_ids.add(registry[mod])

    for doc_id in relevant_doc_ids:
        if doc_id in dynamic_patterns:
            for pattern in dynamic_patterns[doc_id]:
                for line_idx, line in enumerate(lines):
                    if pattern in line:
                        if any(kw in line for kw in ["// noqa: UP", "// noqa: CHUB", "/* noqa: CHUB */"]):
                            continue
                        violations.append({
                            "filename": str(f),
                            "location": {"row": line_idx + 1, "column": line.find(pattern) + 1},
                            "code": "CHUB",
                            "message": f"`{pattern}` is flagged as deprecated or incorrect by chub docs.",
                            "_synth_mod": next((k for k, v in registry.items() if v == doc_id), doc_id.split("/")[0])
                        })

    # 2. JS Quality & Best Practices (The "WOW" Factor)
    JS_QUALITY_RULES = [
        (r'\bvar\s+\w+', "Legacy `var` detected. Use `let` or `const` for modern block-scoping.", "javascript/base"),
        (r"require\(['\"]request['\"]\)", "The `request` library is deprecated. Use `axios`, `node-fetch`, or native `fetch`.", "request/package"),
        (r"\.writeFileSync\(", "Blocking synchronous IO detected. Use `fs.promises.writeFile` or `fs.writeFile` to keep the event loop responsive.", "nodejs/fs"),
        (r"\.readFileSync\(", "Blocking synchronous IO detected. Use `fs.promises.readFile` for better performance.", "nodejs/fs"),
    ]
    
    for pattern, msg, mod_hint in JS_QUALITY_RULES:
        for line_idx, line in enumerate(lines):
            if any(kw in line for kw in ["// noqa", "/* noqa"]):
                continue
            match = re.search(pattern, line)
            if match:
                violations.append({
                    "filename": str(f),
                    "location": {"row": line_idx + 1, "column": match.start() + 1},
                    "code": "CHUB",
                    "message": msg,
                    "_synth_mod": mod_hint
                })

    # Build a set of deprecated component names from all relevant patterns
    # e.g. "openai.ChatCompletion.create" → {"ChatCompletion", "create"}
    # e.g. "from langchain.chat_models import ChatOpenAI" → {"ChatOpenAI", "langchain.chat_models"}
    deprecated_components = {}  # component_name → (doc_id, full_pattern)
    for doc_id in relevant_doc_ids:
        patterns = dynamic_patterns.get(doc_id, [])
        for pattern in patterns:
            # Split dotted patterns into components
            parts = re.split(r'[\s.]+', pattern)
            for part in parts:
                clean = part.strip("()'\"`)").strip()
                if clean and len(clean) > 2 and clean not in {"import", "from", "as", "const", "let", "var", "new", "require"}:
                    # Only flag significant names (start with uppercase or are multi-segment)
                    if clean[0].isupper() or "." in pattern:
                        if clean not in deprecated_components:
                            deprecated_components[clean] = (doc_id, pattern)

    # Scan each line for pattern matches
    for line_idx, line in enumerate(lines):
        if "// noqa: CHUB" in line or "# noqa: CHUB" in line:
            continue

        matched_this_line = set()

        # Strategy 1: Direct string matching against full patterns
        for doc_id in relevant_doc_ids:
            patterns = dynamic_patterns.get(doc_id, [])
            for pattern in patterns:
                if pattern in line:
                    mod_key = next((k for k, v in registry.items() if v == doc_id), doc_id.split("/")[0])
                    if mod_key not in matched_this_line:
                        matched_this_line.add(mod_key)
                        violations.append({
                            "filename": str(f),
                            "location": {"row": line_idx + 1, "column": line.find(pattern) + 1},
                            "code": "CHUB",
                            "message": f"`{pattern}` is flagged as deprecated by chub docs.",
                            "_synth_mod": mod_key,
                        })

        # Strategy 2: Cross-reference imported names against deprecated pattern components
        # Extract names imported on this line
        imported_names = set()
        # import { ChatCompletion, Completion } from 'openai'
        m = re.match(r"""import\s+\{([^}]+)\}\s+from\s+['"]([^'"]+)['"]""", line.strip())
        if m:
            for name in m.group(1).split(","):
                imported_names.add(name.strip().split(" as ")[0].strip())
        # import OpenAI from 'openai'
        m = re.match(r"""import\s+(\w+)\s+from\s+['"]([^'"]+)['"]""", line.strip())
        if m:
            imported_names.add(m.group(1))
        # const { Anthropic } = require(...)
        m = re.match(r"""(?:const|let|var)\s+\{([^}]+)\}\s*=\s*require""", line.strip())
        if m:
            for name in m.group(1).split(","):
                imported_names.add(name.strip().split(":")[0].strip())

        for name in imported_names:
            if name in deprecated_components:
                doc_id, full_pattern = deprecated_components[name]
                mod_key = next((k for k, v in registry.items() if v == doc_id), doc_id.split("/")[0])
                if mod_key not in matched_this_line:
                    matched_this_line.add(mod_key)
                    violations.append({
                        "filename": str(f),
                        "location": {"row": line_idx + 1, "column": max(1, line.find(name) + 1)},
                        "code": "CHUB",
                        "message": f"`{name}` is deprecated (from pattern: `{full_pattern}`). See chub docs.",
                        "_synth_mod": mod_key,
                    })

        # GAP 4 — Strategy 3: Scan all lines for usage of deprecated component names
        for comp_name, (doc_id, full_pattern) in deprecated_components.items():
            # Check if this component name appears in the line as a usage
            # (not just as an import declaration)
            # Avoid re-flagging import lines already caught by Strategy 1/2
            if comp_name in line:
                # Skip if this is an actual import/require/include declaration line (already handled)
                is_import_line = bool(
                    re.match(r"""\s*import\s+.*from\s+['"]""", line) or
                    re.match(r"""\s*import\s+['"]""" , line) or
                    re.match(r"""^\s*#include\s*[<"]""", line) or
                    re.match(r"""^\s*import\s+([a-zA-Z0-9_.]+)""", line) or
                    (re.search(r"""require\s*\(\s*['"]""", line) and re.match(r'\s*(const|let|var)\s', line))
                )
                if is_import_line:
                    continue
                # Skip if already flagged this line for this component
                already_flagged = any(
                    v["location"]["row"] == line_idx + 1 and comp_name in v["message"]
                    for v in violations
                )
                if already_flagged:
                    continue

                mod_key = next((k for k, v in registry.items() if v == doc_id), doc_id.split("/")[0])
                violations.append({
                    "filename": str(f),
                    "location": {"row": line_idx + 1, "column": max(1, line.find(comp_name) + 1)},
                    "code": "CHUB",
                    "message": f"`{comp_name}` is deprecated (from pattern: `{full_pattern}`). See chub docs.",
                    "_synth_mod": mod_key,
                })

    return violations


def get_pinned_versions() -> dict[str, str]:
    """Extract pinned package versions from requirements.txt, pyproject.toml, and package.json."""
    versions = {}

    # requirements.txt
    req_path = REPO_ROOT / "requirements.txt"
    if req_path.exists():
        try:
            for line in req_path.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "==" in line:
                    parts = line.split("==", 1)
                    pkg = parts[0].strip().split("[")[0]  # handle extras like pkg[extra]==1.0
                    ver = parts[1].strip().split(";")[0].strip()  # handle markers
                    if pkg and ver:
                        versions[pkg] = ver
        except Exception:
            pass

    # pyproject.toml (basic parsing)
    pyproject_path = REPO_ROOT / "pyproject.toml"
    if pyproject_path.exists():
        try:
            content = pyproject_path.read_text(encoding="utf-8", errors="replace")
            for m in re.findall(r'"([a-zA-Z0-9_-]+)==([^"]+)"', content):
                versions[m[0]] = m[1]
            for m in re.findall(r"'([a-zA-Z0-9_-]+)==([^']+)'", content):
                versions[m[0]] = m[1]
        except Exception:
            pass

    # package.json
    pkg_json_path = REPO_ROOT / "package.json"
    if pkg_json_path.exists():
        try:
            pkg_data = json.loads(pkg_json_path.read_text(encoding="utf-8", errors="replace"))
            for dep_key in ["dependencies", "devDependencies"]:
                deps = pkg_data.get(dep_key, {})
                if isinstance(deps, dict):
                    for pkg_name, ver_str in deps.items():
                        clean_ver = re.sub(r'^[^0-9]*', '', str(ver_str))
                        if clean_ver:
                            simple_name = pkg_name.split("/")[-1] if "/" in pkg_name else pkg_name
                            versions[simple_name] = clean_ver
                            versions[pkg_name] = clean_ver
        except Exception:
            pass

    return versions


def _get_severity(message: str) -> str:
    """Determine severity based on violation message content."""
    msg_lower = message.lower()
    if "deprecated" in msg_lower:
        return "🔴 Breaking"
    elif "legacy" in msg_lower:
        return "🟡 Warning"
    return "🔵 Info"


# ── GAP 2: Language-aware hint extraction ────────────────────────────

def extract_chub_hint(doc_path: Path, lang: str = "python") -> str | None:
    if not doc_path.exists():
        return None
    content = doc_path.read_text(encoding="utf-8", errors="replace")

    lang_fence = f"```{lang}" if lang != "python" else "```python"

    def _find_hint_in_content(fence: str) -> str | None:
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
                if line.strip().startswith(fence) and not in_code_block:
                    in_code_block = True
                    continue
                elif line.strip().startswith("```") and in_code_block:
                    break

                if in_code_block:
                    code_lines.append(line)

        # Fallback: if no specific section found, just grab the very first matching code block in the document
        if not code_lines:
            in_code_block = False
            for line in content.splitlines():
                if line.strip().startswith(fence) and not in_code_block:
                    in_code_block = True
                    continue
                elif line.strip().startswith("```") and in_code_block:
                    break

                if in_code_block:
                    code_lines.append(line)

        if code_lines:
            return "\n".join(code_lines)
        return None

    # Try the requested language fence first
    result = _find_hint_in_content(lang_fence)
    if result:
        return result

    # Fallback: for JS, try ```javascript then ```js then ```typescript
    if lang == "javascript":
        for fallback_fence in ["```js", "```typescript", "```ts"]:
            result = _find_hint_in_content(fallback_fence)
            if result:
                return result

    # Final fallback: try any code block
    if lang != "python":
        result = _find_hint_in_content("```python")
        if result:
            return result

        # Controlled fallback: try known language fences only
        for safe_fence in ["```python", "```javascript", "```js", "```typescript", "```ts", "```java", "```cpp", "```c"]:
            result = _find_hint_in_content(safe_fence)
            if result:
                return result
        return None


# ── GAP 6: Historical deprecations database ─────────────────────────

def _load_historical_db() -> dict[str, list[str]]:
    """Load historical deprecation patterns from local cache + GitHub source."""
    db = {}

    # Try to fetch from GitHub (cached for 24 hours)
    needs_fetch = True
    if HISTORICAL_DB_PATH.exists():
        mtime = HISTORICAL_DB_PATH.stat().st_mtime
        if (time.time() - mtime) < 86400:
            needs_fetch = False

    if needs_fetch:
        try:
            req = urllib.request.Request(
                HISTORICAL_DB_URL,
                headers={'User-Agent': 'chub-guard/1.2.1'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                HISTORICAL_DB_PATH.write_bytes(response.read())
        except Exception:
            pass  # Offline is fine — use local cache

    if HISTORICAL_DB_PATH.exists():
        try:
            db = json.loads(HISTORICAL_DB_PATH.read_text(encoding="utf-8"))
        except Exception:
            db = {}

    return db


def _update_historical_db(doc_id: str, patterns: list[str]) -> None:
    """Persist newly discovered patterns into the local historical database."""
    if not patterns:
        return
    try:
        db = {}
        if HISTORICAL_DB_PATH.exists():
            db = json.loads(HISTORICAL_DB_PATH.read_text(encoding="utf-8"))
        existing = set(db.get(doc_id, {}).get("patterns", []))
        
        # Identify truly new patterns that we haven't seen before locally
        
        merged = list(existing | set(patterns))
        db[doc_id] = {
            "patterns": merged,
            "last_updated": datetime.datetime.now().strftime("%Y-%m-%d")
        }
        HISTORICAL_DB_PATH.write_text(json.dumps(db, indent=2) + "\n", encoding="utf-8")
            
    except Exception:
        pass


def _sync_global_db():
    """Fetch the latest global deprecations from GitHub if the local cache is > 24h old."""
    if not HISTORICAL_DB_PATH.exists():
        HISTORICAL_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        HISTORICAL_DB_PATH.write_text("{}", encoding="utf-8")
    
    mtime = HISTORICAL_DB_PATH.stat().st_mtime
    if (time.time() - mtime) < 86400:
        return # Recently synced
    
    try:
        console.print("[dim]Syncing global deprecation database from GitHub...[/dim]")
        req = urllib.request.Request(HISTORICAL_DB_URL, headers={'User-Agent': 'chub-guard/1.2.1'})
        with urllib.request.urlopen(req, timeout=10) as response:
            remote_data = json.loads(response.read().decode("utf-8"))
        
        local_data = json.loads(HISTORICAL_DB_PATH.read_text(encoding="utf-8"))
        
        # Merge remote into local
        for doc_id, data in remote_data.items():
            if doc_id not in local_data:
                local_data[doc_id] = data
            else:
                existing = set(local_data[doc_id].get("patterns", []))
                incoming = set(data.get("patterns", []))
                local_data[doc_id]["patterns"] = sorted(list(existing | incoming))
                local_data[doc_id]["last_updated"] = data.get("last_updated", local_data[doc_id]["last_updated"])
        
        HISTORICAL_DB_PATH.write_text(json.dumps(local_data, indent=2) + "\n", encoding="utf-8")
        os.utime(HISTORICAL_DB_PATH, (time.time(), time.time()))
        console.print("[green]✓ Global database synced.[/green]")
    except Exception as e:
        console.print(f"[dim]Note: Could not sync global database (offline or URL moved): {e}[/dim]")

@click.group()
def cli():
    pass

_ADVANCED_RULES = {
    "context_manager_required": [
        # (call_name, message, mod_hint)
        ("aiohttp.ClientSession", "aiohttp.ClientSession() should be used with `async with` to ensure proper connection pooling and cleanup.", "aiohttp"),
        ("ClientSession", "aiohttp.ClientSession() should be used with `async with` to ensure proper connection pooling and cleanup.", "aiohttp"),
    ],
    "deprecated_kwargs": [
        # (call_name, kwarg_name, message, mod_hint)
        ("Accelerator", "fp16", "Argument `fp16=True` is deprecated in `Accelerator`. Use `mixed_precision='fp16'` instead.", "accelerate"),
    ]
}

class PythonAdvancedAnalyzer(ast.NodeVisitor):
    def __init__(self, filename, content, registry):
        self.filename = filename
        self.content = content
        self.lines = content.splitlines()
        self.registry = registry
        self.violations = []
        self.current_async_with = []

    def visit_AsyncWith(self, node):
        self.current_async_with.append(node)
        self.generic_visit(node)
        self.current_async_with.pop()

    def visit_Call(self, node):
        # Context manager rules
        for call_name, msg, mod_hint in _ADVANCED_RULES["context_manager_required"]:
            if self._is_call_to(node, call_name):
                is_in_async_with_header = any(
                    isinstance(item, ast.withitem) and item.context_expr == node
                    for aw in self.current_async_with for item in aw.items
                )
                if not is_in_async_with_header:
                    self.add_violation(node, msg, mod_hint)

        # Deprecated kwargs rules
        for call_name, kwarg_name, msg, mod_hint in _ADVANCED_RULES["deprecated_kwargs"]:
            if self._is_call_to(node, call_name):
                for kw in node.keywords:
                    if kw.arg == kwarg_name:
                        self.add_violation(node, msg, mod_hint)

        self.generic_visit(node)

    def _is_call_to(self, node, name):
        if isinstance(node.func, ast.Name) and node.func.id == name.split('.')[-1]:
            return True
        if isinstance(node.func, ast.Attribute):
            full_name = self._get_full_name(node.func)
            if full_name == name:
                return True
        return False

    def _get_full_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            prefix = self._get_full_name(node.value)
            if prefix:
                return f"{prefix}.{node.attr}"
        return None

    def add_violation(self, node, msg, mod_hint=None):
        self.violations.append({
            "filename": str(self.filename),
            "location": {"row": node.lineno, "column": node.col_offset + 1},
            "code": "CHUB",
            "message": msg,
            "_synth_mod": mod_hint
        })


@cli.command(name="scan")
@click.argument("filenames", nargs=-1, type=click.Path(exists=True, path_type=Path))
@click.option('--json', 'as_json', is_flag=True, default=False)
def scan(filenames, as_json):
    """Run the deprecation guard. If no files are provided, it scans the entire project."""
    if as_json:
        console.quiet = True

    _sync_global_db()
    
    # ── File Discovery ──
    input_files = list(filenames)
    if not input_files:
        # Default to all project files if no arguments provided
        input_files = [REPO_ROOT]
    
    all_files = []
    for path in input_files:
        if path.is_dir():
            # Recursively find all supported file types
            for ext in [".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx"]:
                all_files.extend(path.rglob(f"*{ext}"))
        else:
            all_files.append(path)

    # De-duplicate and filter out ignored directories
    final_files = []
    ignored_patterns = {"node_modules", "venv", ".venv", "env", ".env", "__pycache__", "dist", "build", ".git", ".github", ".chub-docs"}
    
    for f in set(all_files):
        # Check if any part of the path is in ignored_patterns or starts with a dot (except current dir '.')
        try:
            rel_parts = f.resolve().relative_to(REPO_ROOT.resolve()).parts
        except ValueError:
            rel_parts = f.parts
            
        if any(p in ignored_patterns or (p.startswith(".") and p != ".") for p in rel_parts):
            continue
            
        if f.is_file():
            final_files.append(f)

    py_files = [f for f in final_files if f.suffix == ".py"]
    js_files = [f for f in final_files if f.suffix in NON_PY_EXTENSIONS]
    
    if not py_files and not js_files:
        if filenames:
            console.print("[yellow]⚠ No supported files found in the provided paths.[/yellow]")
        else:
            console.print("[yellow]⚠ No supported files found in the project root.[/yellow]")
        sys.exit(0)

    try:
        raw = REGISTRY_PATH.read_bytes()
        # Handle various BOMs from PowerShell/editors
        if raw.startswith(b'\xff\xfe') or raw.startswith(b'\xfe\xff'):
            text = raw.decode('utf-16')
        elif raw.startswith(b'\xef\xbb\xbf'):
            text = raw.decode('utf-8-sig')
        else:
            text = raw.decode('utf-8')
        registry = json.loads(text)
    except FileNotFoundError:
        registry = {}
    except Exception as e:
        # If file exists but is unreadable/corrupt, start with empty registry
        console.print(f"[yellow]⚠ Registry unreadable ({e}), starting with empty registry.[/yellow]")
        registry = {}

    file_to_modules = {}
    all_needed_docs = set()
    for f in py_files:
        modules = get_imported_modules(f)
        file_to_modules[f] = modules
        for mod in modules:
            if mod in registry:
                all_needed_docs.add(registry[mod])

    # ── GAP 7: Cold start registry bootstrap ────────────────────────
    LOCAL_REGISTRY_MIN_ENTRIES = 3
    if len(registry) < LOCAL_REGISTRY_MIN_ENTRIES:
        console.print("[dim]First run detected — bootstrapping registry from full project scan...[/dim]")
        global_lookup, _ = _load_global_chub_registry()
        if global_lookup:
            for pattern in ["**/*.py", "**/*.js", "**/*.ts", "**/*.jsx", "**/*.tsx", "**/*.java", "**/*.c", "**/*.cpp"]:
                for f in REPO_ROOT.rglob(pattern.split("/")[-1]):
                    parts = f.relative_to(REPO_ROOT).parts
                    if any(p.startswith(".") or p in (
                        "node_modules", "venv", ".venv", "__pycache__"
                    ) for p in parts):
                        continue
                    try:
                        mods = get_imported_modules(f) if f.suffix == ".py" else get_js_imports(f)
                        for mod in mods:
                            if mod not in registry and mod in global_lookup:
                                registry[mod] = global_lookup[mod]
                                all_needed_docs.add(global_lookup[mod])
                    except Exception:
                        continue
            try:
                REGISTRY_PATH.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
                console.print(f"[dim]Registry bootstrapped with {len(registry)} entries.[/dim]")
            except Exception:
                pass

    # ── Registry gap warning ─────────────────────────────────────────

    unknown_modules = set()
    for f in py_files:
        for mod in file_to_modules[f]:
            if mod not in registry and len(mod) > 2 and "." not in mod:
                if mod not in STDLIB_MODS:
                    unknown_modules.add(mod)

    # Collect JS imports and needed docs
    js_file_to_modules = {}
    js_needed_docs = set()
    for f in js_files:
        modules = get_js_imports(f)
        js_file_to_modules[f] = modules
        for mod in modules:
            if mod in registry:
                js_needed_docs.add(registry[mod])
            if mod not in registry and len(mod) > 2 and "." not in mod:
                if mod not in STDLIB_MODS:
                    unknown_modules.add(mod)

    # Auto-resolve unknown modules from global chub registry
    if unknown_modules:
        global_lookup, _ = _load_global_chub_registry()
        auto_resolved = {}
        still_unknown = set()
        for mod in unknown_modules:
            if mod in global_lookup:
                doc_id = global_lookup[mod]
                if doc_id not in registry.values():
                    auto_resolved[mod] = doc_id
            else:
                still_unknown.add(mod)
        
        if auto_resolved:
            for mod, doc_id in sorted(auto_resolved.items()):
                registry[mod] = doc_id
                all_needed_docs.add(doc_id)
                console.print(f"[green]✓ Auto-resolved `{mod}` → {doc_id} (from global chub registry)[/green]")
            # Persist the updated local registry
            try:
                REGISTRY_PATH.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
            except Exception:
                pass
        
        # Re-check unknowns: some might have been resolved by another name (alias)
        really_unknown = set()
        for mod in still_unknown:
            # Check if this module or any of its parts already resolve to a doc_id in registry
            # e.g., if "@angular/core" is imported, "angular" might be in registry.
            parts = mod.replace("@", "").split("/")
            # Check for the full mod, the stripped mod, and the top-level part
            possible_keys = {mod, mod.replace("@", ""), parts[0] if parts else mod}
            if any(k in registry for k in possible_keys):
                continue
            really_unknown.add(mod)

        for mod in sorted(really_unknown):
            if mod in global_lookup:
                console.print(f"[yellow]⚠ `{mod}` has chub docs but isn't mapped locally. "
                              f"Run: python scripts/chub_guard.py update-registry[/yellow]")
            # else: chub has no docs for this module — silently skip

    py_needed_docs = set(all_needed_docs)

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    chub_cmd = shutil.which("chub")
    chub_available = chub_cmd is not None
    if not chub_available:
        console.print("[dim]Note: chub CLI not found. Using GitHub fallback for live documentation.[/dim]")

    # ── Version-aware doc fetching ───────────────────────────────────
    pinned = get_pinned_versions()
    _, doc_id_to_langs = _load_global_chub_registry()

    # Consolidate all docs to fetch
    all_docs_to_fetch = []
    for doc_id in py_needed_docs:
        all_docs_to_fetch.append((doc_id, "python"))
    for doc_id in js_needed_docs:
        all_docs_to_fetch.append((doc_id, "javascript"))

    for doc_id, preferred_lang in all_docs_to_fetch:
        safe_name = doc_id.replace("/", "__")
        suffix = "__js" if preferred_lang == "javascript" else ""
        doc_path = DOCS_DIR / f"{safe_name}{suffix}.md"
        
        needs_fetch = True
        if doc_path.exists():
            mtime = doc_path.stat().st_mtime
            if (time.time() - mtime) < 86400:
                needs_fetch = False

        if needs_fetch:
            # Determine which languages to try based on registry info
            available_langs = doc_id_to_langs.get(doc_id, [])
            fetch_langs = []
            if preferred_lang in available_langs:
                fetch_langs.append(preferred_lang)
            
            # Fallbacks
            if preferred_lang == "javascript":
                for fallback in ["typescript", "javascript", "python"]:
                    if fallback in available_langs and fallback not in fetch_langs:
                        fetch_langs.append(fallback)
            elif preferred_lang == "python":
                if "python" not in fetch_langs:
                    fetch_langs.append("python")
            
            # If registry has no info, use defaults
            if not fetch_langs:
                fetch_langs = [preferred_lang]
                if preferred_lang == "javascript":
                    fetch_langs.append("typescript")

            success = False
            tried_langs = []
            for lang in fetch_langs:
                tried_langs.append(lang)
                if chub_available:
                    try:
                        # Always fetch the LATEST documentation to act as a proactive Upgrade Guard
                        version_args = [] 
                        res = subprocess.run(
                            [chub_cmd, "get", doc_id, "--lang", lang, "--output", str(doc_path)] + version_args,
                            timeout=30,
                            capture_output=True,
                            check=False
                        )
                        if res.returncode == 0:
                            success = True
                            # Also fetch full reference if possible (Latest)
                            full_path = DOCS_DIR / f"{safe_name}{suffix}__full.md"
                            subprocess.run(
                                [chub_cmd, "get", doc_id, "--lang", lang, "--full", "--output", str(full_path)],
                                timeout=45, capture_output=True, check=False
                            )
                            break
                    except Exception:
                        pass

                # Github Fallback (try each language)
                if not success:
                    try:
                        parts = doc_id.split("/")
                        if len(parts) == 2:
                            pkg, doc = parts
                            url = f"https://raw.githubusercontent.com/andrewyng/context-hub/main/content/{pkg}/docs/{doc}/{lang}/DOC.md"
                            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                            with urllib.request.urlopen(req, timeout=15) as response:
                                doc_path.write_bytes(response.read())
                            success = True
                            console.print(f"[green]✓ Github fallback fetch ({lang}) successful for {doc_id}[/green]")
                            break
                    except Exception:
                        pass
            
            if success:
                try:
                    rel_path = doc_path.relative_to(REPO_ROOT)
                except ValueError:
                    rel_path = doc_path
                console.print(f"[green]✓ {preferred_lang.upper()} docs resolved ({tried_langs[-1]}) → {rel_path}[/green]")
            else:
                console.print(f"[yellow]⚠ Failed to resolve docs for {doc_id} in any of: {fetch_langs}[/yellow]")

    # ── Ruff linting (Python only) ───────────────────────────────────
    ruff_output = []
    if py_files:
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

    # Build dynamic patterns (GAP 1: now uses polarity-aware extraction)
    dynamic_patterns = {}
    for doc_id in all_needed_docs:
        safe_name = doc_id.replace("/", "__")
        doc_path = DOCS_DIR / f"{safe_name}.md"
        dynamic_patterns[doc_id] = get_dynamic_deprecations(doc_path)

    # Also build JS dynamic patterns from JS-specific docs
    js_dynamic_patterns = {}
    for doc_id in js_needed_docs:
        safe_name = doc_id.replace("/", "__")
        js_doc_path = DOCS_DIR / f"{safe_name}__js.md"
        js_dynamic_patterns[doc_id] = get_js_dynamic_deprecations(js_doc_path)
        # Also include patterns from the Python doc (many are language-agnostic)
        if doc_id in dynamic_patterns:
            js_dynamic_patterns[doc_id] = list(set(js_dynamic_patterns[doc_id] + dynamic_patterns[doc_id]))

    # ── GAP 6: Load historical DB and merge with current dynamic patterns ──
    hist_db = _load_historical_db()
    for doc_id in list(dynamic_patterns.keys()):
        current = dynamic_patterns[doc_id]
        # Update historical DB with newly found patterns
        _update_historical_db(doc_id, current)
        # Merge historical patterns into current detection
        historical = hist_db.get(doc_id, {}).get("patterns", [])
        dynamic_patterns[doc_id] = list(set(current + historical))

    for doc_id in list(js_dynamic_patterns.keys()):
        current = js_dynamic_patterns[doc_id]
        # Update historical DB with newly found patterns
        _update_historical_db(doc_id, current)
        # Merge historical patterns into current detection
        historical = hist_db.get(doc_id, {}).get("patterns", [])
        js_dynamic_patterns[doc_id] = list(set(current + historical))

    # Synthesize CHUB violations for known deprecated AI SDK patterns
    for f in py_files:
        content = f.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
        tree = None
        
        try:
            tree = ast.parse(content)
        except Exception as e:
            # Fallback for SyntaxError (e.g. Python 2 code)
            if isinstance(e, SyntaxError):
                # Run Regex-based INTERNAL_QUALITY_PRESETS scan (Python 2 / Legacy)
                INTERNAL_QUALITY_PRESETS = [
                    (r'\bprint\s+["\']', "Legacy Python 2 `print` statement detected. Use `print()` function.", "python/base"),
                    (r'except\s+\w+,\s+\w+:', "Legacy Python 2 `except` syntax detected. Use `except Exception as e:`.", "python/base"),
                    (r'\burllib2\b', "`urllib2` is deprecated/removed in Python 3. Use `urllib.request` or `requests`.", "urllib2"),
                    (r'\bxrange\b', "`xrange` is removed in Python 3. Use `range`.", "python/base"),
                ]
                for pattern, msg, mod in INTERNAL_QUALITY_PRESETS:
                    for line_idx, line in enumerate(lines):
                        match = re.search(pattern, line)
                        if match:
                            ruff_output.append({
                                "filename": str(f),
                                "location": {"row": line_idx + 1, "column": match.start() + 1},
                                "code": "CHUB",
                                "message": msg,
                                "_synth_mod": mod
                            })

        # 1. Advanced AST Analysis (Only if parse succeeded)
        if tree:
            analyzer = PythonAdvancedAnalyzer(f, content, registry)
            analyzer.visit(tree)
            ruff_output.extend(analyzer.violations)

        def add_synth(line, col, mod, msg):
            if line - 1 < len(lines) and any(kw in lines[line - 1] for kw in ["# noqa: UP", "# noqa: CHUB"]):
                return
            # Prevent duplicates
            if not any(v["location"]["row"] == line and v.get("_synth_mod") == mod for v in ruff_output):
                ruff_output.append({
                    "filename": str(f),
                    "location": {"row": line, "column": col},
                    "code": "CHUB",
                    "message": msg,
                    "_synth_mod": mod
                })

        # 2. Dynamic text matching against chub guidelines (ALWAYS RUNS)
        for line_idx, line in enumerate(lines):
            if any(kw in line for kw in ["# noqa: UP", "# noqa: CHUB"]):
                continue
            for doc_id, patterns in dynamic_patterns.items():
                for pattern in patterns:
                    if pattern in line:
                        mod_key = next((k for k, v in registry.items() if v == doc_id), doc_id.split("/")[0])
                        add_synth(line_idx + 1, line.find(pattern) + 1, mod_key, f"`{pattern}` is flagged as deprecated or incorrect by chub docs.")

        # 3. Automation Quality Presets (Safety net) (ALWAYS RUNS)
        AUTOMATION_PRESETS = [
            (r'\bfind_element_by_\w+', "Deprecated Selenium locator method. Use `find_element(By.ID, ...)` syntax.", "selenium"),
            (r'\bwaitForSelector\(', "Redundant `waitForSelector` detected. Modern Playwright actions (click, fill) auto-wait.", "playwright"),
        ]
        for pattern, msg, mod in AUTOMATION_PRESETS:
            for line_idx, line in enumerate(lines):
                match = re.search(pattern, line)
                if match:
                    add_synth(line_idx + 1, match.start() + 1, mod, msg)

    # ── JS/TS analysis ───────────────────────────────────────────────
    for f in js_files:
        js_violations = analyze_js_file(f, registry, js_dynamic_patterns)
        
        # Advanced JS Rule: Angular mixed with React
        imports = get_js_imports(f)
        if ("react" in imports or "react-dom" in imports) and ("angular" in imports or "@angular/core" in imports):
            js_violations.append({
                "filename": str(f),
                "location": {"row": 1, "column": 1},
                "code": "CHUB",
                "message": "Improper scoping: Found Angular and React imports in the same file. Frameworks should not be mixed within the same component scope.",
                "_synth_mod": "angular"
            })

        ruff_output.extend(js_violations)

    violations = []
    for item in ruff_output:
        code = item.get("code", "")
        # Remove the strict UP filter to allow both ruff and chub issues in the report
            
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
            # GAP 2: Pass correct language for hint extraction
            is_js = str(file_path).endswith(tuple(NON_PY_EXTENSIONS))
            hint = extract_chub_hint(doc_path, lang="javascript" if is_js else "python")
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

    if as_json:
        import json as _json
        output = []
        for v in violations:
            output.append({
                "filename": str(v.filename),
                "location": {"row": v.line, "column": v.col},
                "code": v.code,
                "message": v.message,
                "chub_hint": v.chub_hint,
                "doc_id": v.doc_id,
            })
        print(_json.dumps(output))
        sys.exit(0)

    if not violations:
        # Be silent if running as a pre-commit hook (filenames provided)
        # to match standard linter behavior.
        if not filenames:
            console.print("[green]✓ No deprecated API calls detected[/green]")
        sys.exit(0)

    ai_violations = [v for v in violations if v.code == "CHUB" and Path(str(v.filename)).suffix == ".py"]
    js_chub_violations = [v for v in violations if v.code == "CHUB" and Path(str(v.filename)).suffix in JS_TS_EXTENSIONS]
    c_chub_violations = [v for v in violations if v.code == "CHUB" and Path(str(v.filename)).suffix in C_EXTENSIONS]
    java_chub_violations = [v for v in violations if v.code == "CHUB" and Path(str(v.filename)).suffix in JAVA_EXTENSIONS]
    python_violations = [v for v in violations if v.code != "CHUB"]
    all_chub_violations = ai_violations + js_chub_violations + c_chub_violations + java_chub_violations

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

    # ── AI SDK Violations table ──────────────────────────────────────
    seen_hints = {}  # doc_id → chub_hint (deduplicate)
    if ai_violations:
        ai_table = Table(
            show_header=True,
            header_style="bold green",
            border_style="dim",
            title="[bold green]✦ AI SDK Deprecations (Chub)[/bold green]",
            pad_edge=True,
            expand=True,
        )
        ai_table.add_column("#", style="dim", width=4, justify="right")
        ai_table.add_column("File", style="yellow", no_wrap=True, ratio=3)
        ai_table.add_column("Line", style="magenta", width=6, justify="right")
        ai_table.add_column("Severity", width=12)
        ai_table.add_column("Issue", ratio=6)

        for idx, v in enumerate(ai_violations, 1):
            issue = Text(v.message)
            if v.doc_id:
                issue.append(f"  [{v.doc_id}]", style="dim")
            severity = _get_severity(v.message)
            ai_table.add_row(str(idx), str(v.filename), str(v.line), severity, issue)
            if v.chub_hint and v.doc_id and v.doc_id not in seen_hints:
                seen_hints[v.doc_id] = v.chub_hint
        console.print(ai_table)
        console.print()

    # ── Python Violations table ──────────────────────────────────────
    if python_violations:
        py_table = Table(
            show_header=True,
            header_style="bold cyan",
            border_style="dim",
            title="[bold cyan]🐍 Python Deprecations & Issues (Ruff)[/bold cyan]",
            pad_edge=True,
            expand=True,
        )
        py_table.add_column("#", style="dim", width=4, justify="right")
        py_table.add_column("File", style="yellow", no_wrap=True, ratio=3)
        py_table.add_column("Line", style="magenta", width=6, justify="right")
        py_table.add_column("Code", style="cyan", width=8)
        py_table.add_column("Issue", ratio=6)

        for idx, v in enumerate(python_violations, 1):
            py_table.add_row(str(idx), str(v.filename), str(v.line), v.code, v.message)
        console.print(py_table)

    # ── JS/TS Violations table ───────────────────────────────────────
    if js_chub_violations:
        js_table = Table(
            show_header=True,
            header_style="bold yellow",
            border_style="dim",
            title="[bold yellow]🟨 JS/TS Deprecations (Chub)[/bold yellow]",
            pad_edge=True,
            expand=True,
        )
        js_table.add_column("#", style="dim", width=4, justify="right")
        js_table.add_column("File", style="yellow", no_wrap=True, ratio=3)
        js_table.add_column("Line", style="magenta", width=6, justify="right")
        js_table.add_column("Severity", width=12)
        js_table.add_column("Issue", ratio=6)

        for idx, v in enumerate(js_chub_violations, 1):
            issue = Text(v.message)
            if v.doc_id:
                issue.append(f"  [{v.doc_id}]", style="dim")
            severity = _get_severity(v.message)
            js_table.add_row(str(idx), str(v.filename), str(v.line), severity, issue)
            if v.chub_hint and v.doc_id and v.doc_id not in seen_hints:
                seen_hints[v.doc_id] = v.chub_hint
        console.print(js_table)
        console.print()

    if c_chub_violations:
        c_table = Table(
            show_header=True,
            header_style="bold red",
            border_style="dim",
            title="[bold red]⚙ C/C++ Deprecations (Chub)[/bold red]",
            pad_edge=True,
            expand=True,
        )
        c_table.add_column("#", style="dim", width=4, justify="right")
        c_table.add_column("File", style="red", no_wrap=True, ratio=3)
        c_table.add_column("Line", style="magenta", width=6, justify="right")
        c_table.add_column("Severity", width=12)
        c_table.add_column("Issue", ratio=6)

        for idx, v in enumerate(c_chub_violations, 1):
            issue = Text(v.message)
            if v.doc_id:
                issue.append(f"  [{v.doc_id}]", style="dim")
            severity = _get_severity(v.message)
            c_table.add_row(str(idx), str(v.filename), str(v.line), severity, issue)
            if v.chub_hint and v.doc_id and v.doc_id not in seen_hints:
                seen_hints[v.doc_id] = v.chub_hint
        console.print(c_table)
        console.print()

    if java_chub_violations:
        java_table = Table(
            show_header=True,
            header_style="bold blue",
            border_style="dim",
            title="[bold blue]☕ Java Deprecations (Chub)[/bold blue]",
            pad_edge=True,
            expand=True,
        )
        java_table.add_column("#", style="dim", width=4, justify="right")
        java_table.add_column("File", style="blue", no_wrap=True, ratio=3)
        java_table.add_column("Line", style="magenta", width=6, justify="right")
        java_table.add_column("Severity", width=12)
        java_table.add_column("Issue", ratio=6)

        for idx, v in enumerate(java_chub_violations, 1):
            issue = Text(v.message)
            if v.doc_id:
                issue.append(f"  [{v.doc_id}]", style="dim")
            severity = _get_severity(v.message)
            java_table.add_row(str(idx), str(v.filename), str(v.line), severity, issue)
            if v.chub_hint and v.doc_id and v.doc_id not in seen_hints:
                seen_hints[v.doc_id] = v.chub_hint
        console.print(java_table)
        console.print()

    # ── Chub hints (one per SDK) ────────────────────────────────────
    if seen_hints:
        console.print()
        console.print(Rule("[bold green]RECOMMENDED FIXES[/bold green]", style="green"))
        console.print()
        for doc_id, hint_code in seen_hints.items():
            # Determine syntax highlighting based on hint content
            hint_lang = "python"
            if any(kw in hint_code for kw in ["import ", "require(", "const ", "let ", "=> "]):
                # Check if it looks more like JS
                if "require(" in hint_code or "const " in hint_code or "=> " in hint_code:
                    hint_lang = "javascript"
            hint_panel = Syntax(hint_code, hint_lang, theme="monokai", line_numbers=False, word_wrap=True)
            # Determine correct lang flag for subtitle
            hint_lang_flag = "python"
            if hint_code and any(kw in hint_code for kw in ["require(", "const ", "let ", "import ", "=> "]):
                if not any(kw in hint_code for kw in ["import ast", "import os", "def ", "class ", "    return"]):
                    hint_lang_flag = "javascript"
                    
            console.print(Panel(
                hint_panel,
                title=f"[bold green]✦ {doc_id}[/bold green]",
                subtitle=f"[dim]chub get {doc_id} --lang {hint_lang_flag}[/dim]",
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

    # Read existing report early for trend calculation
    existing = ""
    if report_path.exists():
        try:
            existing = report_path.read_text(encoding="utf-8")
        except Exception:
            existing = ""

    # Build this run's section
    run_lines = [
        f"## 🕐 Run: {timestamp}",
        "",
        f"**{len(violations)}** issue{'s' if len(violations) != 1 else ''} found across **{len(file_counts)}** file{'s' if len(file_counts) != 1 else ''}.",
        "",
        "### 🛡️ Upgrade Readiness",
        "Your project was scanned against the **LATEST** documentation from Context-Hub to ensure you are aware of upcoming deprecations and migration paths.",
        "",
        "### 📦 Local Environment",
        "The following versions are currently installed/pinned in your project:",
    ]
    pinned = get_pinned_versions()
    if pinned:
        for pkg, ver in sorted(pinned.items()):
            run_lines.append(f"- `{pkg}`: {ver}")
    else:
        run_lines.append("- (No pinned versions detected, using latest documentation)")
    run_lines.append("")

    # ── Trend line ───────────────────────────────────────────────────
    prev_run_match = re.search(r"\*\*(\d+)\*\* issue.*?across \*\*(\d+)\*\* file", existing)
    if prev_run_match:
        prev_count = int(prev_run_match.group(1))
        delta = len(violations) - prev_count
        if delta < 0:
            trend = f"↓ {abs(delta)} fewer than last run"
        elif delta > 0:
            trend = f"↑ {delta} more than last run"
        else:
            trend = "→ same as last run"
        run_lines.append(f"*Trend: {trend}*")
        run_lines.append("")

    if ai_violations:
        run_lines += [
            "### ✦ AI SDK Deprecations",
            "",
            "| # | File | Line | Severity | Issue |",
            "|---|------|------|----------|-------|",
        ]
        for idx, v in enumerate(ai_violations, 1):
            issue_text = v.message
            if v.doc_id:
                issue_text += f" *[{v.doc_id}]*"
            issue_text = issue_text.replace("|", "\\|")
            fname = str(v.filename).replace("\\", "/")
            severity = _get_severity(v.message)
            run_lines.append(f"| {idx} | `{fname}` | {v.line} | {severity} | {issue_text} |")
        run_lines.append("")

    if python_violations:
        run_lines += [
            "### 🐍 Python Deprecations & Issues",
            "",
            "| # | File | Line | Code | Issue |",
            "|---|------|------|------|-------|",
        ]
        for idx, v in enumerate(python_violations, 1):
            issue_text = v.message.replace("|", "\\|")
            fname = str(v.filename).replace("\\", "/")
            run_lines.append(f"| {idx} | `{fname}` | {v.line} | `{v.code}` | {issue_text} |")
        run_lines.append("")

    if js_chub_violations:
        run_lines += [
            "### 🟨 JS/TS Deprecations (Chub)",
            "",
            "| # | File | Line | Severity | Issue |",
            "|---|------|------|----------|-------|",
        ]
        for idx, v in enumerate(js_chub_violations, 1):
            issue_text = v.message
            if v.doc_id:
                issue_text += f" *[{v.doc_id}]*"
            issue_text = issue_text.replace("|", "\\|")
            fname = str(v.filename).replace("\\", "/")
            severity = _get_severity(v.message)
            run_lines.append(f"| {idx} | `{fname}` | {v.line} | {severity} | {issue_text} |")
        run_lines.append("")

    if c_chub_violations:
        run_lines += [
            "### ⚙ C/C++ Deprecations (Chub)",
            "",
            "| # | File | Line | Severity | Issue |",
            "|---|------|------|----------|-------|",
        ]
        for idx, v in enumerate(c_chub_violations, 1):
            issue_text = v.message.replace("|", "\\|")
            fname = str(v.filename).replace("\\", "/")
            severity = _get_severity(v.message)
            run_lines.append(f"| {idx} | `{fname}` | {v.line} | {severity} | {issue_text} |")
        run_lines.append("")

    if java_chub_violations:
        run_lines += [
            "### ☕ Java Deprecations (Chub)",
            "",
            "| # | File | Line | Severity | Issue |",
            "|---|------|------|----------|-------|",
        ]
        for idx, v in enumerate(java_chub_violations, 1):
            issue_text = v.message.replace("|", "\\|")
            fname = str(v.filename).replace("\\", "/")
            severity = _get_severity(v.message)
            run_lines.append(f"| {idx} | `{fname}` | {v.line} | {severity} | {issue_text} |")
        run_lines.append("")

    if seen_hints:
        run_lines += [
            "",
            "### Recommended Fixes",
        ]
        for doc_id, hint_code in seen_hints.items():
            # Detect hint language for correct fence
            _fence_lang = "python"
            if hint_code:
                # Check for JS keywords
                js_kws = ["require(", "const ", "let ", "=> ", "async function", "await fetch", "npm install"]
                py_kws = ["def ", "class ", "import ast", "    return", "pip install"]
                
                js_score = sum(1 for kw in js_kws if kw in hint_code)
                py_score = sum(1 for kw in py_kws if kw in hint_code)
                
                # If it's a JS/TS file, favor JS
                if any(str(v.filename).endswith(tuple(NON_PY_EXTENSIONS)) for v in violations if v.doc_id == doc_id):
                    js_score += 2
                
                if js_score > py_score:
                    _fence_lang = "javascript"

            run_lines += [
                "",
                f"#### ✦ `{doc_id}`",
                "",
                f"```{_fence_lang}",
                hint_code,
                "```",
                "",
                f"> Full docs: `chub get {doc_id} --lang {_fence_lang}`",
            ]

    run_lines += [
        "",
        "### 🤖 Agent Prompt",
        "",
        "Copy this into your coding agent to fix all issues:",
        "",
        '> "Fix all issues in this chub_guard report.',
        "> For AI SDK deprecations use the recommended fix blocks above.",
        "> For Python deprecations apply standard pyupgrade fixes.",
        "> For JS/TS deprecations use the modern SDK patterns from chub docs.",
        '> Do not change any logic — only fix deprecated patterns."',
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
        if existing:
            # Extract the previous "latest" run's timestamp + summary as a one-liner
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
        console.print()
        console.print(Panel(
            f"[bold green]📊 REPORT GENERATED[/bold green]\n\n"
            f"A detailed markdown report has been saved to:\n"
            f"[cyan]{report_path.resolve()}[/cyan]\n\n"
            f"[dim]Use this report to fix issues across your entire project.[/dim]",
            border_style="green",
            padding=(1, 2)
        ))
    except Exception as e:
        console.print(f"[yellow]⚠ Could not write report: {e}[/yellow]")

    # Only block commit if there are real violations
    total_blocking = len(ai_violations) + len(js_chub_violations) + len(c_chub_violations) + len(java_chub_violations) + len(python_violations)
    if total_blocking > 0:
        sys.exit(1)


@cli.command()
def update_registry():
    """Scan project imports and auto-populate local registry from global chub registry."""
    global_lookup, _ = _load_global_chub_registry()
    if not global_lookup:
        console.print("[red]Error: Global chub registry not found at ~/.chub/sources/default/registry.json[/red]")
        console.print("[dim]Install chub first: npm install -g context-hub[/dim]")
        sys.exit(1)

    console.print(f"[dim]Global chub registry loaded: {len(global_lookup)} package mappings[/dim]")

    try:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except Exception:
        registry = {}

    # Scan all .py, .js, .ts files in the project for imports
    all_imports = set()
    for pattern in ["**/*.py", "**/*.js", "**/*.ts", "**/*.jsx", "**/*.tsx"]:
        for f in REPO_ROOT.rglob(pattern.split("/")[-1]):
            # Skip hidden dirs, node_modules, venv, .chub-docs
            parts = f.relative_to(REPO_ROOT).parts
            if any(p.startswith(".") or p in ("node_modules", "venv", ".venv", "__pycache__") for p in parts):
                continue
            try:
                if f.suffix == ".py":
                    mods = get_imported_modules(f)
                else:
                    mods = get_js_imports(f)
                all_imports.update(mods.keys())
            except Exception:
                continue

    console.print(f"[dim]Found {len(all_imports)} unique imports across project[/dim]")

    new_entries = {}
    for mod in sorted(all_imports):
        if mod in registry:
            continue
        if mod in STDLIB_MODS:
            continue
        if len(mod) <= 2 or "." in mod:
            continue
        if mod in global_lookup:
            doc_id = global_lookup[mod]
            if doc_id not in registry.values():
                new_entries[mod] = doc_id

    if not new_entries:
        console.print("[green]✓ Local registry is up to date — all resolvable imports are mapped.[/green]")
        return

    console.print(f"\n[cyan]Found {len(new_entries)} new mappings:[/cyan]")
    for k, v in sorted(new_entries.items()):
        console.print(f"  [yellow]{k}[/yellow] → [green]{v}[/green]")

    if click.confirm(f"\nAdd {len(new_entries)} entries to registry.json?"):
        registry.update(new_entries)
        REGISTRY_PATH.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
        console.print(f"[green]✓ Registry updated with {len(new_entries)} new entries.[/green]")


def _is_quality_pattern(pattern: str) -> bool:
    """Return True if pattern is worth promoting to global database."""
    p = pattern.strip()
    # Minimum length
    if len(p) < 6:
        return False
    # Must contain at least one dot or space (import path or call chain)
    if "." not in p and " " not in p:
        return False
    # Skip pure punctuation or numeric strings
    if re.match(r'^[^a-zA-Z]+$', p):
        return False
    # Skip single generic words
    generic = {"create", "update", "delete", "get", "set", "run", "start",
               "stop", "init", "build", "load", "save", "read", "write",
               "open", "close", "connect", "send", "receive", "request",
               "response", "error", "success", "fail", "check", "test"}
    if p.lower() in generic:
        return False
    return True

@cli.command()
def promote_deprecations():
    """Merge locally discovered patterns from cache into root deprecations.json for global sync."""
    root_db_path = REPO_ROOT / "deprecations.json"
    if not root_db_path.exists():
        root_db_path.write_text("{}", encoding="utf-8")
    
    try:
        local_db = json.loads(HISTORICAL_DB_PATH.read_text(encoding="utf-8")) if HISTORICAL_DB_PATH.exists() else {}
        root_db = json.loads(root_db_path.read_text(encoding="utf-8"))
        
        merged_count = 0
        for doc_id, data in local_db.items():
            if doc_id not in root_db:
                root_db[doc_id] = {"patterns": [], "last_updated": ""}
            
            existing = set(root_db[doc_id].get("patterns", []))
            incoming = set(p for p in data.get("patterns", []) if _is_quality_pattern(p))
            
            new_patterns = incoming - existing
            if new_patterns:
                merged_count += len(new_patterns)
                root_db[doc_id]["patterns"] = sorted(list(existing | incoming))
                root_db[doc_id]["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d")
        
        if merged_count > 0:
            root_db_path.write_text(json.dumps(root_db, indent=2) + "\n", encoding="utf-8")
            console.print(f"[green]✓ Successfully promoted {merged_count} new patterns to root `deprecations.json`[/green]")
            console.print("[dim]Next step: `git add deprecations.json && git commit -m 'Update global patterns' && git push`[/dim]")
        else:
            console.print("[yellow]No new patterns to promote — root `deprecations.json` is already up to date.[/yellow]")
            
    except Exception as e:
        console.print(f"[red]Error promoting deprecations: {e}[/red]")


# Add run as an alias for scan to support existing git hooks
cli.add_command(scan, name="run")

if __name__ == "__main__":
    cli()
