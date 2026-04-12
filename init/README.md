# chub-guard-init

One command to set up [chub_guard](https://github.com/rhealaloo45/chub-guard)
in any project.

## Prerequisites

- Node >= 18
- Python + pip
- git

## Usage

Run once in any new project:

    npx chub-guard-init

This will:
- Copy `chub_guard.py` into `scripts/`
- Write `.pre-commit-config.yaml`
- Write `.chub-docs/registry.json`
- Run `pre-commit install` automatically

## After Setup

Install chub so the guard can fetch live docs:

    npm install -g @aisuite/chub

Make a commit to test it:

    git commit -m "test"

## Suppressing False Positives

Add `# noqa: UP035` to any line to skip:

    import google.generativeai as genai  # noqa: UP035

## Updating the Registry

    python scripts/chub_guard.py update-registry

## Part of chub-guard

This is the installer for chub_guard.
Full docs: https://github.com/rhealaloo45/chub-guard
