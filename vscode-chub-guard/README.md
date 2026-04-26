# chub-guard for VS Code

Real-time detection of deprecated AI SDK patterns, automation APIs, and legacy code.

## Features

- Red squiggles on deprecated lines as you code
- Side panel listing all violations with file + line
- Jump directly to any deprecated line with one click
- Fix manually (check off as you go) or send report to your coding agent
- Pause/resume pre-commit hook from the panel
- Force commit bypass when needed
- Auto-installs chub-guard-init if not present in project

## Requirements

- Python 3.10+
- pipx or pip (for auto-setup)
- git (for hook management)

## Setup

Install the extension. On first activation in any workspace, it automatically
runs `pipx run chub-guard-init` to set up the guard. No manual steps needed.

## Hiding the Panel

If the panel is too noisy, click "Hide panel on save" at the bottom.
Use the command palette: `chub-guard: Scan Now` to trigger manually.

## Commands

- `chub-guard: Scan Now` — manual scan
- `chub-guard: Pause Pre-commit Hook` — stop blocking commits temporarily  
- `chub-guard: Resume Pre-commit Hook` — re-enable blocking
- `chub-guard: Hide Panel on Save` — suppress auto-open
- `chub-guard: Show Panel on Save` — re-enable auto-open

## Suppressing False Positives

Add `# noqa: CHUB` to any line in Python, or `// noqa: CHUB` in JS/TS.

## Part of chub-guard

Full docs: https://github.com/rhealaloo45/chub-guard
