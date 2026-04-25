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

## Automated Community Intelligence (Telemetry)
* **Silent Webhook Integration:** Implemented a `_send_telemetry` function in `chub_guard.py` that intercepts newly discovered deprecation patterns locally and silently POSTs them to a central webhook server hosted on Render.com.
* **Zero-Friction Global Sync:** The Render server acts as an intermediary, using a GitHub token to automatically merge and commit these new patterns into the global `rhealaloo45/chub-guard/deprecations.json` registry.
* **Failsafe Execution:** The telemetry is wrapped in a strict 2-second timeout `try/except` block, ensuring offline developers or server outages never block the core `git commit` process.
