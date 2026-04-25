import shutil
import subprocess
import sys
from pathlib import Path

# Package-relative assets (for installed version)
PACKAGE_DIR = Path(__file__).parent
ASSETS_DIR  = PACKAGE_DIR / "assets"

# Repository-relative fallback (for development version)
REPO_ROOT   = PACKAGE_DIR.parent.parent

def get_asset(filename: str, repo_path: Path) -> str:
    """Read asset from package directory or fallback to repo path."""
    installed_path = ASSETS_DIR / filename
    if installed_path.exists():
        return installed_path.read_text(encoding="utf-8")
    
    # Fallback to repo root if running from source
    dev_path = REPO_ROOT / repo_path
    if dev_path.exists():
        return dev_path.read_text(encoding="utf-8")
    
    raise FileNotFoundError(f"Missing essential asset: {filename}.\nSearched:\n  - {installed_path}\n  - {dev_path}")

CHUB_GUARD_PY   = get_asset("chub_guard.py", Path("scripts/chub_guard.py"))
PRE_COMMIT_YAML = get_asset(".pre-commit-config.yaml", Path(".pre-commit-config.yaml"))
REGISTRY_JSON   = get_asset("registry.json", Path(".chub-docs/registry.json"))


def is_pre_commit_installed() -> bool:
    return shutil.which("pre-commit") is not None


def is_git_repo(cwd: Path) -> bool:
    return (cwd / ".git").exists()


def ask(question: str) -> str:
    try:
        return input(question).strip().lower()
    except (EOFError, KeyboardInterrupt):
        return "n"


def safe_write(file_path: Path, content: str, label: str) -> None:
    if file_path.exists():
        answer = ask(f"⚠ {label} already exists. Overwrite? (y/n): ")
        if answer != "y":
            print(f"  skipped {label}")
            return
    try:
        file_path.write_text(content, encoding="utf-8")
        print(f"✓ {label}")
    except Exception as e:
        print(f"✗ Failed to write {label}: {e}")


def main() -> None:
    args = sys.argv[1:]
    if args and args[0] == "run-all":
        cwd = Path.cwd()
        guard_path = cwd / "scripts" / "chub_guard.py"
        if not guard_path.exists():
            print("❌ Error: chub_guard.py not found in scripts/. Run 'chub-guard-init' first.")
            sys.exit(1)
        
        print("")
        print("🚀 Running chub-guard on all project files...")
        print("───────────────────────────────────────")
        try:
            # Use sys.executable to ensure we use the same python interpreter if possible, 
            # otherwise fallback to 'python'
            py_cmd = sys.executable if sys.executable else "python"
            subprocess.run([py_cmd, str(guard_path), "run"], check=True)
            sys.exit(0)
        except subprocess.CalledProcessError as e:
            sys.exit(e.returncode)
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)

    cwd = Path.cwd()

    print("")
    print("chub-guard-init")
    print("───────────────────────────────────────")
    print("Setting up chub_guard in this project...")
    print("")

    # 1. Create directories
    (cwd / "scripts").mkdir(parents=True, exist_ok=True)
    (cwd / ".chub-docs").mkdir(parents=True, exist_ok=True)

    # 2. Write files
    safe_write(cwd / "scripts" / "chub_guard.py",      CHUB_GUARD_PY,   "scripts/chub_guard.py")
    safe_write(cwd / ".pre-commit-config.yaml",         PRE_COMMIT_YAML, ".pre-commit-config.yaml")
    safe_write(cwd / ".chub-docs" / "registry.json",   REGISTRY_JSON,   ".chub-docs/registry.json")

    # 3. Update .gitignore
    gitignore_path = cwd / ".gitignore"
    gitignore_entry = ".chub-docs/*.md"
    if gitignore_path.exists():
        content = gitignore_path.read_text(encoding="utf-8")
        if gitignore_entry not in content:
            gitignore_path.write_text(content.rstrip() + f"\n{gitignore_entry}\n", encoding="utf-8")
            print("✓ .gitignore updated")
    else:
        gitignore_path.write_text(f"{gitignore_entry}\n", encoding="utf-8")
        print("✓ .gitignore created")

    print("")

    # 4. Check for git repo
    if not is_git_repo(cwd):
        print("⚠ No .git directory found.")
        print("  Run git init first, then: pre-commit install")
        print("")
        sys.exit(0)

    # 5. Run pre-commit install
    if is_pre_commit_installed():
        try:
            subprocess.run(["pre-commit", "install"], cwd=cwd, check=True)
            print("")
            print("✓ pre-commit hook installed")
            print("")
            print("───────────────────────────────────────")
            print("Done! chub_guard will now run on every commit.")
            print("")
            print("Next steps:")
            print("  1. Install chub:  npm install -g @aisuite/chub")
            print("  2. Make a commit to test the guard")
            print("")
        except subprocess.CalledProcessError:
            print("⚠ pre-commit install failed. Run manually: pre-commit install")
    else:
        print("⚠ pre-commit not found. To finish setup:")
        print("")
        print("  pip install pre-commit")
        print("  pre-commit install")
        print("")
        print("Then install chub: npm install -g @aisuite/chub")


if __name__ == "__main__":
    main()
