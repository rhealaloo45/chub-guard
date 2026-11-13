# System Changes Log

This file documents the architectural changes made to `chub_guard.py` and the surrounding infrastructure during our current session.

## Multi-Language Extension
* **Pattern Upgrades:** Expanded `JS_EXTENSIONS` to support `.c`, `.cpp`, `.cc`, `.cxx`, `.h`, `.hpp`, `.hxx`, and `.java`.
* **Regex Engine Updates:** Replaced basic string matching in `get_js_imports` (now acting as a broad `get_regex_imports`) with support for parsing `#include <...>` headers and Java `import ...;` statements.
* **Auto-Normalization:** Java packages utilizing dot notation (`openai.package`) are automatically replaced with slash notation internally (`openai/package`) to ensure they resolve natively against the `~/.chub/sources/default/registry.json` database.
* **Complex Import Parsing:** Re-wrote JavaScript Regex matches to intercept complex destructured imports (e.g., `import React, { Component } from 'react'`) which previously returned `None`.

## False-Positive Reductions
* **Doc-Fetch Language Handling:** Fixed a bug causing `chub get <package> --lang python` to fire uniformly across `.jsx` and `.tsx` files. The system now dynamically parses `--lang javascript` to the chub CLI if pulling JS-oriented frameworks (like `antd` or `react`).
* **Fuzzy String Trimming Removed:** Overrode a legacy `chub_guard` function (`p.split('.')[0]`) that indiscriminately stripped characters off deprecation rules (converting `client.beta` -> `client` and `import React` -> `React`). The script now enforces strictly **full pattern matching**, entirely eliminating innocent keyword collisions with common variables like `client` or `async`.

## Registry Intelligence Updates
* **Global GitHub Sync:** Every 24 hours, the tool automatically fetches the latest community-contributed patterns from the global GitHub database and merges them into the local cache.

## Unreleased: current code is no longer flagged

* **Fix:** the doc reader treated any name mentioned near a warning word as deprecated, so advice like "Do not treat `message.content` as a single string" flagged the call itself, along with `client.chat.completions.create` and `response.text`. Patterns that a doc's own current examples use are now dropped (`_current_usage`), as are bare version numbers such as `1.2.11`.
* **Fix (JS/TS):** deprecated *names* are only class-like identifiers (`ChatCompletion`, `LLMChain`) and are matched as whole words, so `client`, `create` and `openai` are no longer flagged on any line that contains them.
* On 13 labelled snippets against the live docs, the 1.2.1 rules caught 18 of 19 deprecated lines with 11 wrong flags on current code; with this change, 18 of 19 with none.
* `CHUB_GUARD_LEGACY=1` runs the 1.2.1 rules unchanged. Tests: `tests/test_current_usage.py`.
* Not yet released: the version is still 1.2.1 in every package until the next publish.

## v1.2.1: The Universal Guard
* **Branding Shift:** Rebranded from a specialized AI SDK linter to a Universal Deprecation Guard for modern engineering projects.
* **Expanded Scope:** Added native support for identifying "Everything" deprecations:
    * **Browser Automation**: Selenium and Playwright pattern matching.
    * **Legacy Python**: Python 2 syntax and deprecated stdlib module detection.
    * **Framework Smells**: Multi-framework import conflict detection (React + Angular).
* **Documentation Overhaul:** Updated all READMEs (Root, Pip, npm) and System Overviews to reflect the universal safety net positioning.
* **Structural Intelligence:** Implemented a new `PythonAdvancedAnalyzer` (AST Visitor) that identifies "deep context" smells previously invisible to regex:
    * **Async Management**: Detects `aiohttp.ClientSession` usage outside of `async with` blocks.
    * **Keyword Arguments**: Flags deprecated arguments like `Accelerator(fp16=True)` while ignoring valid calls.
* **Resilient Engine**: Decoupled the Regex Pass from the AST loop, ensuring Selenium and Chub-doc patterns are detected even in files with syntax errors (legacy code support).
* **Version Sync:** Unified all components under the `1.2.1` major version tag.


