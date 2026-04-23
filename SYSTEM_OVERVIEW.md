# System Overview: chub Deprecation Guard

This document explains the internal architecture, design decisions, and execution flow of the `chub_guard.py` CLI tool.

## Core Objective
The goal of the tool is to bridge the gap between static analysis and rapidly evolving third-party AI SDKs. Standard tools like `ruff` or `eslint` often lag behind rapidly shipped AI tools. The `chub Deprecation Guard` introduces a mechanism to dynamically inject AI SDK deprecation rules into the linting pipeline using live documentation fetched directly from the context-hub registry.

## Architecture Flow

The tool executes via a pipeline during the `pre-commit` stage, or via manual CLI execution:

### 1. File Collection & Multi-Language Parsing
When triggered, the script receives a list of staged Python (`.py`) and JavaScript/TypeScript (`.js`, `.jsx`, `.ts`, `.tsx`) files.
*   **Python:** Uses Python's built-in `ast` (Abstract Syntax Tree) module to safely parse the source code and discover `import` and `from ... import` statements.
*   **JS/TS:** Uses a robust Regex-based system to extract imported module definitions, identifying named imports, default imports, scoped packages (`@namespace/pkg`), and `require()` statements.

### 2. Global & Local Registry Resolution
The script cross-references discovered modules against the local project configuration (`.chub-docs/registry.json`).
*   **Global Integration:** If an imported module is missing from the local registry, the tool automatically scans the global chub registry (`~/.chub/sources/default/registry.json`, containing 1500+ mappings). If a match is found, the package is auto-resolved and added to the local setup, totally eliminating manual config steps.
*   **Registry Gap Warning:** Modules that are entirely unknown trigger a warning, advising the user to check their packages.
*   **Auto-Update Command:** A dedicated `update-registry` command exists to scan the entire codebase against the global mappings and safely populate missing configurations, excluding standard library files automatically.

### 3. Version-Aware Documentation Fetching & Caching
For matched SDKs, the tool attempts to fetch the latest Markdown documentation via the `chub` CLI:
*   **Version Pinning:** `chub_guard` intelligently parses `requirements.txt`, `pyproject.toml`, and `package.json` to extract exact pinned versions of the dependencies. It dynamically passes these limits to the CLI (e.g. `chub get <pkg> --version 1.5.0`).
*   **Language-Specific Docs:** Fetch commands append the detected file's extension (`--lang python` or `--lang js`) to get accurate API signatures.
*   **Cache & Fallback:** Fetched documents are cached in `.chub-docs/` for 24 hours. If `chub` is unavailable or fails due to missing language implementations, it attempts an HTTP fallback request to the raw GitHub URL.

### 4. Hybrid Deprecation Analysis
The analysis system strictly avoids static hardcoding, driving all rules dynamically:

**Dynamic Markdown Parsing:**
The tool dynamically reads the downloaded `chub` markdown file. It uses Regular Expressions to scan for code snippets wrapped in backticks (e.g., \`ChatCompletion\`) that appear on lines containing negative keywords like `"incorrect"`, `"deprecated"`, `"legacy"`, `"do not"`, or `"avoid"`.

It then scans the staged files for these dynamically extracted patterns:
*   **Python:** Performs substring checks on text nodes, generating `CHUB` violations on matching components.
*   **JS/TS Cross-Referencing:** Because Javascript imports often destructure features (e.g., `import { ChatCompletion } from "openai"`), matching Python-centric doc strings like `openai.ChatCompletion.create` directly against lines fails. Instead, the tool extracts names specific to current imports, isolating components (`ChatCompletion`), and flags their usage if they appear in any deprecated document strings.

### 5. Standard Linting Integration
For Python, the tool executes `ruff check --select UP --output-format json` to catch standard Python pyupgrade violations natively. 
It merges its dynamically synthesized AI SDK violations (labeled as `CHUB`) into the combined pipeline.

### 6. Rich Reporting & Agent Handoff
If violations are found, the tool provides human and machine-readable output:
*   **Rich UI Terminal Rendering:** It draws standard tables identifying File paths, Line Numbers, severity metrics (🔴 Breaking, 🟡 Warning, 🔵 Info), and extracted API fixes found under the `"## Usage"` sections in documentation.
*   **Markdown Reports:** Automatically generates and updates `chub_guard_report.md` at the project root for IDE accessibility.
*   **Historical Tracking & Trends:** Compares previous runs to compute trends (`↑`, `↓`, or `→`).
*   **Autonomous Agent Prompting:** Integrates an `Agent Prompt` section formatting the broken code alongside its required syntax update. This section is specifically structurally designed to copy/paste into LLMs or for native execution by autonomous agentic workspaces.

## Edge Cases Handled

1. **Duplicate Blocking:** The synthesis engine checks if a violation has already been logged for a specific line/module to prevent spamming the user.
2. **False Positive Suppression:** Before flagging a synthesized violation, the tool checks the raw source line for `# noqa: CHUB` (Python) or `// noqa: CHUB` (JS/TS). If present, the violation is silently dropped.
3. **Graceful Degradation:** If `chub` is completely unreachable and the GitHub fallback fails, the tool emits a yellow warning but continues operation. It will not block a commit simply because the internet is down.
4. **Syntax Errors:** If a staged Python file has a fatal syntax error, the AST parser emits a warning and skips the file rather than crashing the entire hook.
