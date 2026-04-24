# System Overview: chub Deprecation Guard

This document explains the internal architecture, design decisions, and execution flow of the `chub_guard.py` CLI tool.

## Core Objective
The goal of the tool is to bridge the gap between static analysis and rapidly evolving third-party AI SDKs. Standard tools like `ruff` or `eslint` often lag behind rapidly shipped AI tools. The `chub Deprecation Guard` introduces a mechanism to dynamically inject AI SDK deprecation rules into the linting pipeline using live documentation fetched directly from the context-hub registry.

## Architecture Flow

The tool executes via a pipeline during the `pre-commit` stage, or via manual CLI execution:

### 1. File Collection & Multi-Language Parsing
When triggered, the script receives a list of staged files across multiple languages:
*   **Python:** Uses Python's built-in `ast` module to safely parse the source code and discover imports.
*   **JS/TS/React:** Uses a robust Regex-based system to extract imports, identifying named imports, default imports, scoped packages (`@namespace/pkg`), and `require()` statements.
*   **Java/C/C++:** Implements lightweight regex parsing to identify package imports (`import ...`, `#include`) and cross-references them against the global registry.

### 2. Global & Local Registry Resolution
The script cross-references discovered modules against the local project configuration (`.chub-docs/registry.json`).
*   **Global Integration:** If an imported module is missing from the project, the tool automatically scans the global chub registry (`~/.chub/sources/default/registry.json`, containing 3700+ mappings). It auto-normalizes aliases (e.g., mapping `@angular/core` to `angular/core`) and populates the local project setup.
*   **Auto-Bootstrap:** On first run, the tool performs a "Cold Start" scan of the entire repository to build a comprehensive dependency map automatically.

### 3. Version-Aware Documentation Fetching & Caching
For matched SDKs, the tool attempts to fetch the latest Markdown documentation via the `chub` CLI:
*   **Version Pinning:** It intelligently parses `requirements.txt`, `pyproject.toml`, and `package.json` to extract pinned versions and passes them to the CLI (e.g. `chub get <pkg> --version 1.5.0`).
*   **Dynamic Language Selection:** The tool dynamically queries the registry for supported documentation languages. It will attempt primary matches (e.g., `javascript` for `.js` files) but automatically falls back to secondary options like `typescript` if the primary documentation is missing.
*   **Cache & Fallback:** Fetched documents are cached for 24 hours. If `chub` is unavailable, it attempts a language-aware fallback request to raw GitHub URLs.

### 4. Advanced Hybrid Analysis
The analysis system combines high-performance pattern matching with structural code understanding:

**A. Advanced AST Analysis (Python):**
To handle "Deep Context" smells, the tool implements a structural `ast.NodeVisitor`:
*   **Context Management:** Detects if `aiohttp.ClientSession()` is used outside of an `async with` block.
*   **Argument Logic:** Discerning deprecated keyword arguments (e.g., flagging `Accelerator(fp16=True)` but allowing `mixed_precision='fp16'`).

**B. Dynamic Markdown Parsing:**
The tool scans downloaded `chub` markdown for negative keywords (e.g., `"deprecated"`, `"legacy"`) and extracts backticked patterns (`ChatCompletion`) to flag in the source code.

**C. Cross-Framework Scoping (JS/TS):**
Detects architectural misconfigurations, such as improperly mixing `Angular` and `React` imports within the same component file.

### 5. Community Sync Loop
The tool maintains a "living" intelligence database:
*   **Automatic Pull:** Every 24 hours, the tool automatically fetches the latest community-contributed patterns from the global GitHub database and merges them into the local cache.
*   **Contribution (Promote):** Users can run `promote-deprecations` to merge locally learned patterns from their cache into the root `deprecations.json` to share updates with the global community.

### 6. Standard Linting & Reporting
*   **Standard Integration:** Executes `ruff` natively for Python `pyupgrade` (UP) rules and merges results with custom `CHUB` violations.
*   **Rich Reporting:** Generates a unified `chub_guard_report.md` with 🔴 Breaking, 🟡 Warning, and 🔵 Info metrics, alongside trend tracking.
*   **Autonomous Agent Prompting:** Specifically formats code fixes into "Agent Prompt" blocks designed for one-click resolution by AI coding assistants.

## Edge Cases Handled

1. **Duplicate Blocking:** Prevents spamming the same violation across multiple lines.
2. **False Positive Suppression:** Respects `# noqa: CHUB` (Python) or `// noqa: CHUB` (JS/TS) comments.
3. **Graceful Degradation:** Emits warnings on network failure but will not block commits if documentation cannot be fetched.
4. **Syntax Resilience:** Skips files with fatal syntax errors without crashing the entire pipeline.
