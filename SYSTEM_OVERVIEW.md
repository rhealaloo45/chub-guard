# System Overview: chub Deprecation Guard

This document explains the internal architecture, design decisions, and execution flow of the `chub_guard.py` CLI tool.

## Core Objective
The goal of the tool is to bridge the gap between static analysis and rapidly evolving third-party AI SDKs. Standard tools like `ruff` or `eslint` often lag behind rapidly shipped AI tools. The `chub Deprecation Guard` introduces a mechanism to dynamically inject AI SDK deprecation rules into the linting pipeline using live documentation fetched directly from the context-hub registry.

## Architecture Flow

The tool operates as a hybrid background engine that triggers through multiple entry points:

1. **VS Code Extension:** Provides real-time, "as-you-type" feedback with red squiggles and a dedicated issues panel. Distributed via the VS Code Marketplace. (See [vsc_flow.md](file:///Users/rhea/Desktop/Rhea%20Code/chub-guard/vsc_flow.md) for a detailed breakdown).
2. **Git Commit Hook:** Intercepts changes during the `pre-commit` stage to prevent deprecated code from reaching the repository.
3. **Manual CLI Execution:** Allows developers to run full-project audits on demand.

### Multi-Platform Distribution
`chub-guard` is designed for seamless adoption across different environments:
*   **VS Code Marketplace**: Search for `chub-guard` for the easiest, GUI-first experience.
*   **npm**: `npx chub-guard-init` for JS/TS projects.
*   **PyPI**: `pip install chub-guard-init` or `pipx run chub-guard-init` for Python-centric workflows.

### 1. File Collection & Multi-Language Parsing
When triggered, the engine analyzes either the staged files (Hook) or the active file/workspace (IDE):
*   **Python:** Uses Python's built-in `ast` module to safely parse the source code and discover imports.
*   **JS/TS/React:** Uses a robust Regex-based system to extract imports, identifying named imports, default imports, scoped packages (`@namespace/pkg`), and `require()` statements.
*   **Java/C/C++:** Implements lightweight regex parsing to identify package imports (`import ...`, `#include`) and cross-references them against the global registry.

### 2. Global & Local Registry Resolution
The script cross-references discovered modules against the local project configuration (`.chub-docs/registry.json`).
*   **Global Integration:** If an imported module is missing from the project, the tool automatically scans the global chub registry (`~/.chub/sources/default/registry.json`, containing 3700+ mappings). It auto-normalizes aliases (e.g., mapping `@angular/core` to `angular/core`) and populates the local project setup.
*   **Intelligent Skipping:** Standard library imports and unmapped third-party modules that do not exist in the global registry are silently ignored. This prevents unnecessary network requests and minimizes terminal noise.
*   **Auto-Bootstrap:** On first run, the tool performs a "Cold Start" scan of the entire repository to build a comprehensive dependency map automatically.

### 3. Version-Aware Documentation Fetching & Caching
For matched SDKs, the tool attempts to fetch the latest Markdown documentation via the `chub` CLI:
*   **Version Pinning:** It intelligently parses `requirements.txt`, `pyproject.toml`, and `package.json` to extract pinned versions and passes them to the CLI (e.g. `chub get <pkg> --version 1.5.0`).
*   **Dynamic Language Selection:** The tool dynamically queries the registry for supported documentation languages. It will attempt primary matches (e.g., `javascript` for `.js` files) but automatically falls back to secondary options like `typescript` if the primary documentation is missing.
*   **Cache & Fallback:** Fetched documents are cached for 24 hours. If `chub` is unavailable, it attempts a language-aware fallback request to raw GitHub URLs.

### 4. Advanced Hybrid Analysis (The Resilient Engine)
The analysis system combines structural code understanding with high-performance, syntax-agnostic pattern matching to ensure coverage even in legacy or broken files:

**A. Structural AST Analysis (Python):**
Used for high-confidence structural checks when code is syntactically valid:
*   **Context Management:** Detects if `aiohttp.ClientSession()` is used outside of an `async with` block.
*   **Argument Logic:** Discerning deprecated keyword arguments (e.g., flagging `Accelerator(fp16=True)`).

**B. Resilient Regex Fallback (The Safety Net):**
If a file has syntax errors (e.g., Python 2 `print` statements or missing parentheses), the tool **does not skip the file**. Instead, it executes a pure Regex Pass that catches:
*   **Automation Deprecations**: Selenium `find_element_by_*` and Playwright `waitForSelector`.
*   **Legacy Signatures**: Python 2 `urllib2`, `xrange`, and `except Exception, e` syntax.
*   **Dynamic Doc Patterns**: All patterns extracted from Chub markdown docs are checked via regex, ensuring "Upgrade Guard" functionality even during heavy refactoring.

**B. Dynamic Markdown Parsing:**
The tool scans downloaded `chub` markdown for negative keywords (e.g., `"deprecated"`, `"legacy"`) and extracts backticked patterns (`ChatCompletion`) to flag in the source code.

**C. Cross-Framework Scoping (JS/TS):**
Detects architectural misconfigurations, such as improperly mixing `Angular` and `React` imports within the same component file.

### 5. Community Sync Loop
The tool maintains a "living" intelligence database:
*   **Automatic Pull:** Every 24 hours, the tool automatically fetches the latest community-contributed patterns from the global GitHub database and merges them into the local cache.

### 6. Standard Linting & Reporting
*   **Standard Integration:** Executes `ruff` natively for Python `pyupgrade` (UP) rules and merges results with custom `CHUB` violations.
*   **Unified Diagnostics:** In VS Code, violations are surfaced as native Editor Diagnostics (red squiggles).
*   **Interactive Side Panel:** A dedicated VS Code panel lists all violations, allowing developers to jump directly to the code or check off fixed items.
*   **Markdown Reporting:** Generates a project-wide `chub_guard_report.md` with 🔴 Breaking, 🟡 Warning, and 🔵 Info metrics, alongside trend tracking.
*   **Autonomous Agent Prompting:** Specifically formats code fixes into "Agent Prompt" blocks designed for one-click resolution by AI coding assistants.

## Edge Cases Handled

1. **Duplicate Blocking:** Prevents spamming the same violation across multiple lines.
2. **False Positive Suppression:** Universal support for `# noqa: CHUB` or `// noqa: CHUB` inline comments across all languages to permanently suppress false positives.
3. **Graceful Degradation:** Emits warnings on network failure but will not block commits if documentation cannot be fetched.
4. **Syntax Resilience:** Unlike standard linters, the hybrid engine falls back to a Regex-only scan for files with syntax errors. This ensures that a legacy Python 2 file or a broken Selenium script still gets flagged for deprecations without crashing the pipeline.
