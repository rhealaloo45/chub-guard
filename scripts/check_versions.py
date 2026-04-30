#!/usr/bin/env python3
"""VULN-17: Version consistency checker — run in CI to ensure all distributions stay in sync."""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def extract_versions() -> dict[str, str]:
    """Extract version strings from all distribution files."""
    versions = {}

    # 1. Core engine: scripts/chub_guard.py
    guard_py = REPO_ROOT / "scripts" / "chub_guard.py"
    if guard_py.exists():
        content = guard_py.read_text(encoding="utf-8")
        m = re.search(r'^VERSION\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
        if m:
            versions["scripts/chub_guard.py"] = m.group(1)

    # 2. VS Code extension: vscode-chub-guard/package.json
    vscode_pkg = REPO_ROOT / "vscode-chub-guard" / "package.json"
    if vscode_pkg.exists():
        data = json.loads(vscode_pkg.read_text(encoding="utf-8"))
        versions["vscode-chub-guard/package.json"] = data.get("version", "MISSING")

    # 3. npm init package: init/package.json
    npm_pkg = REPO_ROOT / "init" / "package.json"
    if npm_pkg.exists():
        data = json.loads(npm_pkg.read_text(encoding="utf-8"))
        versions["init/package.json"] = data.get("version", "MISSING")

    # 4. pip package: cli/pyproject.toml
    pip_toml = REPO_ROOT / "cli" / "pyproject.toml"
    if pip_toml.exists():
        content = pip_toml.read_text(encoding="utf-8")
        m = re.search(r'^version\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
        if m:
            versions["cli/pyproject.toml"] = m.group(1)

    return versions


def main():
    versions = extract_versions()
    
    if not versions:
        print("ERROR: No version strings found!")
        sys.exit(1)

    unique = set(versions.values())
    
    print("Version strings found:")
    for location, version in sorted(versions.items()):
        status = "OK" if len(unique) == 1 else ("OK" if version == max(unique) else "MISMATCH")
        print(f"  {status} {location}: {version}")
    
    if len(unique) > 1:
        print(f"\nERROR: Version mismatch detected! Found {len(unique)} different versions: {unique}")
        print("All distributions must use the same version string.")
        sys.exit(1)
    else:
        print(f"\nOK All {len(versions)} distributions are at version {unique.pop()}")
        sys.exit(0)


if __name__ == "__main__":
    main()
