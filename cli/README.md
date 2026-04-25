# chub-guard-init (pip)

One command to set up [chub_guard](https://github.com/rhealaloo45/chub-guard) in any Python project.

## Prerequisites

- Python >= 3.10
- pip or pipx
- Node.js/npm (for documentation engine)
- git

## Usage

### Option 1 — pipx (recommended, no permanent install)

    pipx run chub-guard-init

### Option 2 — pip

    pip install chub-guard-init
    chub-guard-init

### Run on demand (Project-wide scan & report)

    pipx run chub-guard-init run-all
    # or
    chub-guard-init run-all

This generates a detailed **`chub_guard_report.md`** in your root directory.

This will:
- **Auto-install** `@aisuite/chub` documentation engine via npm.
- Copy `chub_guard.py` into `scripts/`
- Write `.pre-commit-config.yaml`
- Write `.chub-docs/registry.json`
- Update `.gitignore` to ignore doc caches
- Run `pre-commit install` automatically
- Enable zero-intervention telemetry to sync new AI deprecations globally

## After Setup

The guard will now run automatically on every `git commit`. 

Make a commit to test it:

    git commit -m "test"

## Suppressing False Positives

Add `# noqa: CHUB` (or `// noqa: CHUB` for JS/C/Java) to any line to skip:

    import google.generativeai as genai  # noqa: CHUB

## Also available via npm

    npx chub-guard-init

## Part of chub-guard

Full docs: https://github.com/rhealaloo45/chub-guard
