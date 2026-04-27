# ðŸ›¡ï¸ Chub Guard Report

## ðŸ• Run: 2026-04-27 22:19:57

**135** issues found across **24** files.

### ðŸ›¡ï¸ Upgrade Readiness
Your project was scanned against the **LATEST** documentation from Context-Hub to ensure you are aware of upcoming deprecations and migration paths.

### ðŸ“¦ Local Environment
The following versions are currently installed/pinned in your project:
- (No pinned versions detected, using latest documentation)

*Trend: â†’ same as last run*

### âœ¦ AI SDK Deprecations

| # | File | Line | Severity | Issue |
|---|------|------|----------|-------|
| 1 | `tests/test_chub_guard.py` | 19 | ðŸ”´ Breaking | `google.generativeai` is flagged as deprecated or incorrect by chub docs. *[gemini/genai]* |
| 2 | `tests/test_chub_guard.py` | 54 | ðŸ”´ Breaking | `google.generativeai` is flagged as deprecated or incorrect by chub docs. *[gemini/genai]* |
| 3 | `tests/test_chub_guard.py` | 60 | ðŸ”´ Breaking | `google.generativeai` is flagged as deprecated or incorrect by chub docs. *[gemini/genai]* |
| 4 | `tests/test_chub_guard.py` | 76 | ðŸ”´ Breaking | `ChatCompletion` is flagged as deprecated or incorrect by chub docs. *[openai/package]* |
| 5 | `tests/test_chub_guard.py` | 194 | ðŸ”´ Breaking | `google.generativeai` is flagged as deprecated or incorrect by chub docs. *[gemini/genai]* |
| 6 | `tests/test_chub_guard.py` | 195 | ðŸ”´ Breaking | `google.generativeai` is flagged as deprecated or incorrect by chub docs. *[gemini/genai]* |
| 7 | `cli/chub_guard_init/main.py` | 169 | ðŸ”´ Breaking | `if __name__ == "__main__":` is flagged as deprecated or incorrect by chub docs. *[accelerate/package]* |
| 8 | `cli/chub_guard_init/assets/chub_guard.py` | 51 | ðŸ”´ Breaking | `async` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 9 | `cli/chub_guard_init/assets/chub_guard.py` | 491 | ðŸ”´ Breaking | `ChatCompletion` is flagged as deprecated or incorrect by chub docs. *[openai/package]* |
| 10 | `cli/chub_guard_init/assets/chub_guard.py` | 533 | ðŸ”´ Breaking | `ChatCompletion` is flagged as deprecated or incorrect by chub docs. *[openai/package]* |
| 11 | `cli/chub_guard_init/assets/chub_guard.py` | 599 | ðŸ”´ Breaking | `pyproject.toml` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 12 | `cli/chub_guard_init/assets/chub_guard.py` | 619 | ðŸ”´ Breaking | `pyproject.toml` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 13 | `cli/chub_guard_init/assets/chub_guard.py` | 620 | ðŸ”´ Breaking | `pyproject.toml` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 14 | `cli/chub_guard_init/assets/chub_guard.py` | 621 | ðŸ”´ Breaking | `pyproject` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 15 | `cli/chub_guard_init/assets/chub_guard.py` | 623 | ðŸ”´ Breaking | `pyproject` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 16 | `cli/chub_guard_init/assets/chub_guard.py` | 835 | ðŸ”´ Breaking | `async` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 17 | `cli/chub_guard_init/assets/chub_guard.py` | 836 | ðŸ”´ Breaking | `async` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 18 | `cli/chub_guard_init/assets/chub_guard.py` | 851 | ðŸ”´ Breaking | `async` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 19 | `cli/chub_guard_init/assets/chub_guard.py` | 854 | ðŸ”´ Breaking | `async` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 20 | `cli/chub_guard_init/assets/chub_guard.py` | 855 | ðŸ”´ Breaking | `generic` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 21 | `cli/chub_guard_init/assets/chub_guard.py` | 856 | ðŸ”´ Breaking | `async` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 22 | `cli/chub_guard_init/assets/chub_guard.py` | 862 | ðŸ”´ Breaking | `async` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 23 | `cli/chub_guard_init/assets/chub_guard.py` | 864 | ðŸ”´ Breaking | `async` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 24 | `cli/chub_guard_init/assets/chub_guard.py` | 866 | ðŸ”´ Breaking | `async` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 25 | `cli/chub_guard_init/assets/chub_guard.py` | 876 | ðŸ”´ Breaking | `generic` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 26 | `cli/chub_guard_init/assets/chub_guard.py` | 1703 | ðŸ”´ Breaking | `async` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 27 | `cli/chub_guard_init/assets/chub_guard.py` | 1860 | ðŸ”´ Breaking | `generic` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 28 | `cli/chub_guard_init/assets/chub_guard.py` | 1861 | ðŸ”´ Breaking | `generic` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 29 | `cli/chub_guard_init/assets/chub_guard.py` | 1865 | ðŸ”´ Breaking | `generic` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 30 | `cli/chub_guard_init/assets/chub_guard.py` | 1908 | ðŸ”´ Breaking | `if __name__ == "__main__":` is flagged as deprecated or incorrect by chub docs. *[accelerate/package]* |
| 31 | `scripts/chub_guard.py` | 1714 | ðŸ”´ Breaking | `async` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 32 | `scripts/chub_guard.py` | 1889 | ðŸ”´ Breaking | `generic` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 33 | `scripts/chub_guard.py` | 1890 | ðŸ”´ Breaking | `generic` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 34 | `scripts/chub_guard.py` | 1894 | ðŸ”´ Breaking | `generic` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 35 | `scripts/chub_guard.py` | 1937 | ðŸ”´ Breaking | `if __name__ == "__main__":` is flagged as deprecated or incorrect by chub docs. *[accelerate/package]* |
| 36 | `tests/test_app.py` | 1 | ðŸ”´ Breaking | `google.generativeai` is flagged as deprecated or incorrect by chub docs. *[gemini/genai]* |
| 37 | `init/assets/scripts/chub_guard.py` | 1684 | ðŸ”´ Breaking | `async` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 38 | `init/assets/scripts/chub_guard.py` | 1841 | ðŸ”´ Breaking | `generic` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 39 | `init/assets/scripts/chub_guard.py` | 1842 | ðŸ”´ Breaking | `generic` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 40 | `init/assets/scripts/chub_guard.py` | 1846 | ðŸ”´ Breaking | `generic` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 41 | `init/assets/scripts/chub_guard.py` | 1886 | ðŸ”´ Breaking | `if __name__ == "__main__":` is flagged as deprecated or incorrect by chub docs. *[accelerate/package]* |
| 42 | `tests/test_registry_py.py` | 7 | ðŸ”´ Breaking | Argument `fp16=True` is deprecated in `Accelerator`. Use `mixed_precision='fp16'` instead. *[accelerate/package]* |
| 43 | `tests/test_registry_py.py` | 31 | ðŸ”µ Info | aiohttp.ClientSession() should be used with `async with` to ensure proper connection pooling and cleanup. *[aiohttp/package]* |
| 44 | `tests/test_registry_py.py` | 5 | ðŸ”´ Breaking | `import torch` is flagged as deprecated or incorrect by chub docs. *[torch/package]* |
| 45 | `tests/test_registry_py.py` | 28 | ðŸ”´ Breaking | `async` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 46 | `tests/test_registry_py.py` | 30 | ðŸ”´ Breaking | `async` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 47 | `tests/test_registry_py.py` | 31 | ðŸ”´ Breaking | `async` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 48 | `tests/test_registry_py.py` | 33 | ðŸ”´ Breaking | `resp.text` is flagged as deprecated or incorrect by chub docs. *[aiohttp/package]* |
| 49 | `tests/test_registry_py.py` | 37 | ðŸ”´ Breaking | `async` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 50 | `tests/test_registry_py.py` | 56 | ðŸ”´ Breaking | `import albumentations` is flagged as deprecated or incorrect by chub docs. *[albumentations/package]* |
| 51 | `tests/test_registry_py.py` | 59 | ðŸ”´ Breaking | `A.Compose` is flagged as deprecated or incorrect by chub docs. *[albumentations/package]* |
| 52 | `tests/test_py_gaps.py` | 2 | ðŸ”´ Breaking | `google.generativeai` is flagged as deprecated or incorrect by chub docs. *[gemini/genai]* |
| 53 | `tests/test_py_gaps.py` | 6 | ðŸ”´ Breaking | `ChatCompletion` is flagged as deprecated or incorrect by chub docs. *[openai/package]* |
| 54 | `tests/test_py_gaps.py` | 8 | ðŸ”´ Breaking | `ChatCompletion` is flagged as deprecated or incorrect by chub docs. *[openai/package]* |
| 55 | `tests/test_py_gaps.py` | 9 | ðŸ”´ Breaking | `ChatCompletion` is flagged as deprecated or incorrect by chub docs. *[openai/package]* |

### ðŸŸ¨ JS/TS Deprecations (Chub)

| # | File | Line | Severity | Issue |
|---|------|------|----------|-------|
| 1 | `tests/test_app.ts` | 1 | ðŸ”´ Breaking | `ChatOpenAI` is deprecated (from pattern: `from langchain.chat_models import ChatOpenAI`). See chub docs. *[langchain/package]* |
| 2 | `tests/test_pip.js` | 4 | ðŸ”´ Breaking | `React` is deprecated (from pattern: `import React from "react"`). See chub docs. *[react/react]* |
| 3 | `tests/test_pip.js` | 1 | ðŸ”µ Info | Improper scoping: Found Angular and React imports in the same file. Frameworks should not be mixed within the same component scope. *[angular/core]* |
| 4 | `vscode-chub-guard/out/hookManager.js` | 2 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 5 | `vscode-chub-guard/out/hookManager.js` | 4 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 6 | `vscode-chub-guard/out/hookManager.js` | 13 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 7 | `vscode-chub-guard/out/hookManager.js` | 18 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 8 | `vscode-chub-guard/out/hookManager.js` | 19 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 9 | `vscode-chub-guard/out/hookManager.js` | 21 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 10 | `vscode-chub-guard/out/hookManager.js` | 22 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 11 | `vscode-chub-guard/out/hookManager.js` | 29 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 12 | `vscode-chub-guard/out/hookManager.js` | 30 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 13 | `tests/test_registry_react.js` | 19 | ðŸ”´ Breaking | `import React from "react"` is flagged as deprecated or incorrect by chub docs. *[react/react]* |
| 14 | `tests/test_registry_react.js` | 2 | ðŸ”´ Breaking | `React` is deprecated (from pattern: `import React from "react"`). See chub docs. *[react/react]* |
| 15 | `tests/test_registry_react.js` | 19 | ðŸ”´ Breaking | `import React from "react"` is flagged as deprecated by chub docs. *[react/react]* |
| 16 | `tests/test_registry_react.js` | 22 | ðŸ”´ Breaking | `React` is deprecated (from pattern: `import React from "react"`). See chub docs. *[react/react]* |
| 17 | `tests/test_registry_react.js` | 1 | ðŸ”µ Info | Improper scoping: Found Angular and React imports in the same file. Frameworks should not be mixed within the same component scope. *[angular/core]* |
| 18 | `vscode-chub-guard/out/runner.js` | 2 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 19 | `vscode-chub-guard/out/runner.js` | 4 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 20 | `vscode-chub-guard/out/runner.js` | 13 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 21 | `vscode-chub-guard/out/runner.js` | 18 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 22 | `vscode-chub-guard/out/runner.js` | 19 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 23 | `vscode-chub-guard/out/runner.js` | 21 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 24 | `vscode-chub-guard/out/runner.js` | 22 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 25 | `vscode-chub-guard/out/runner.js` | 29 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 26 | `vscode-chub-guard/out/runner.js` | 30 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 27 | `tests/test_app.js` | 1 | ðŸ”´ Breaking | `ChatCompletion` is flagged as deprecated or incorrect by chub docs. *[openai/package]* |
| 28 | `tests/test_app.js` | 1 | ðŸ”´ Breaking | `ChatCompletion` is flagged as deprecated by chub docs. *[openai/package]* |
| 29 | `tests/test_app.js` | 3 | ðŸ”´ Breaking | `Anthropic` is deprecated (from pattern: `Anthropic().completions.create`). See chub docs. *[anthropic/package]* |
| 30 | `tests/test_react.jsx` | 7 | ðŸ”´ Breaking | `ChatCompletion` is flagged as deprecated or incorrect by chub docs. *[openai/package]* |
| 31 | `tests/test_react.jsx` | 7 | ðŸ”´ Breaking | `ChatCompletion.create` is flagged as deprecated or incorrect by chub docs. *[openai/package]* |
| 32 | `tests/test_react.jsx` | 1 | ðŸ”´ Breaking | `React` is deprecated (from pattern: `import React from "react"`). See chub docs. *[react/react]* |
| 33 | `tests/test_react.jsx` | 7 | ðŸ”´ Breaking | `ChatCompletion` is flagged as deprecated by chub docs. *[openai/package]* |
| 34 | `tests/test_react.jsx` | 8 | ðŸ”´ Breaking | `gpt-3` is deprecated (from pattern: `gpt-3.5-turbo-instruct`). See chub docs. *[openai/package]* |
| 35 | `tests/test_react_node.jsx` | 44 | ðŸ”´ Breaking | `React` is deprecated (from pattern: `import React from "react"`). See chub docs. *[react/react]* |
| 36 | `tests/test_react_node.jsx` | 45 | ðŸ”´ Breaking | `React` is deprecated (from pattern: `import React from "react"`). See chub docs. *[react/react]* |
| 37 | `vscode-chub-guard/out/panel.js` | 2 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 38 | `vscode-chub-guard/out/panel.js` | 4 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 39 | `vscode-chub-guard/out/panel.js` | 13 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 40 | `vscode-chub-guard/out/panel.js` | 18 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 41 | `vscode-chub-guard/out/panel.js` | 19 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 42 | `vscode-chub-guard/out/panel.js` | 21 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 43 | `vscode-chub-guard/out/panel.js` | 22 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 44 | `vscode-chub-guard/out/panel.js` | 29 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 45 | `vscode-chub-guard/out/panel.js` | 30 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 46 | `vscode-chub-guard/out/extension.js` | 2 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 47 | `vscode-chub-guard/out/extension.js` | 4 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 48 | `vscode-chub-guard/out/extension.js` | 13 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 49 | `vscode-chub-guard/out/extension.js` | 18 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 50 | `vscode-chub-guard/out/extension.js` | 19 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 51 | `vscode-chub-guard/out/extension.js` | 21 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 52 | `vscode-chub-guard/out/extension.js` | 22 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 53 | `vscode-chub-guard/out/extension.js` | 29 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 54 | `vscode-chub-guard/out/extension.js` | 30 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 55 | `tests/test_registry_node.jsx` | 7 | ðŸ”´ Breaking | `client` is deprecated (from pattern: `client.completions.create`). See chub docs. *[anthropic/package]* |
| 56 | `tests/test_registry_node.jsx` | 12 | ðŸ”´ Breaking | `client` is deprecated (from pattern: `client.completions.create`). See chub docs. *[anthropic/package]* |
| 57 | `tests/test_mixed_frameworks.jsx` | 1 | ðŸ”´ Breaking | `React` is deprecated (from pattern: `import React from "react"`). See chub docs. *[react/react]* |
| 58 | `tests/test_mixed_frameworks.jsx` | 5 | ðŸ”´ Breaking | `React` is deprecated (from pattern: `import React from "react"`). See chub docs. *[react/react]* |
| 59 | `tests/test_mixed_frameworks.jsx` | 1 | ðŸ”µ Info | Improper scoping: Found Angular and React imports in the same file. Frameworks should not be mixed within the same component scope. *[angular/core]* |
| 60 | `vscode-chub-guard/out/diagnostics.js` | 2 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 61 | `vscode-chub-guard/out/diagnostics.js` | 4 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 62 | `vscode-chub-guard/out/diagnostics.js` | 13 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 63 | `vscode-chub-guard/out/diagnostics.js` | 18 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 64 | `vscode-chub-guard/out/diagnostics.js` | 19 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 65 | `vscode-chub-guard/out/diagnostics.js` | 21 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 66 | `vscode-chub-guard/out/diagnostics.js` | 22 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 67 | `vscode-chub-guard/out/diagnostics.js` | 29 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 68 | `vscode-chub-guard/out/diagnostics.js` | 30 | ðŸŸ¡ Warning | Legacy `var` detected. Use `let` or `const` for modern block-scoping. |
| 69 | `tests/test_js_gaps.js` | 10 | ðŸ”´ Breaking | `ChatCompletion` is flagged as deprecated or incorrect by chub docs. *[openai/package]* |
| 70 | `tests/test_js_gaps.js` | 10 | ðŸ”´ Breaking | `ChatCompletion.create` is flagged as deprecated or incorrect by chub docs. *[openai/package]* |
| 71 | `tests/test_js_gaps.js` | 10 | ðŸ”´ Breaking | `ChatCompletion` is flagged as deprecated by chub docs. *[openai/package]* |
| 72 | `tests/test_js_gaps.js` | 10 | ðŸ”´ Breaking | `gpt-3` is deprecated (from pattern: `gpt-3.5-turbo-instruct`). See chub docs. *[openai/package]* |

### âš™ C/C++ Deprecations (Chub)

| # | File | Line | Severity | Issue |
|---|------|------|----------|-------|
| 1 | `tests/test_cpp.cpp` | 6 | ðŸ”´ Breaking | `ChatCompletion` is flagged as deprecated or incorrect by chub docs. |
| 2 | `tests/test_cpp.cpp` | 6 | ðŸ”´ Breaking | `openai.ChatCompletion.create` is flagged as deprecated or incorrect by chub docs. |
| 3 | `tests/test_cpp.cpp` | 6 | ðŸ”´ Breaking | `ChatCompletion.create` is flagged as deprecated or incorrect by chub docs. |
| 4 | `tests/test_cpp.cpp` | 6 | ðŸ”´ Breaking | `ChatCompletion` is flagged as deprecated by chub docs. |

### â˜• Java Deprecations (Chub)

| # | File | Line | Severity | Issue |
|---|------|------|----------|-------|
| 1 | `tests/test_java.java` | 5 | ðŸ”´ Breaking | `ChatCompletion` is flagged as deprecated or incorrect by chub docs. |
| 2 | `tests/test_java.java` | 6 | ðŸ”´ Breaking | `ChatCompletion` is flagged as deprecated or incorrect by chub docs. |
| 3 | `tests/test_java.java` | 5 | ðŸ”´ Breaking | `ChatCompletion` is flagged as deprecated by chub docs. |
| 4 | `tests/test_java.java` | 6 | ðŸ”´ Breaking | `ChatCompletion` is flagged as deprecated by chub docs. |


### Recommended Fixes

#### âœ¦ `gemini/genai`

```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
  model='gemini-2.5-flash',
  contents='why is the sky blue?',
)

print(response.text) # output is often markdown
```

> Full docs: `chub get gemini/genai --lang python`

#### âœ¦ `openai/package`

```javascript
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    instructions="You are a concise coding assistant.",
    input="How do I reverse a list in Python?",
)

print(response.output_text)
print(response._request_id)
```

> Full docs: `chub get openai/package --lang javascript`

#### âœ¦ `accelerate/package`

```python
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from accelerate import Accelerator

def main() -> None:
    accelerator = Accelerator()

    model = nn.Sequential(nn.Linear(16, 32), nn.ReLU(), nn.Linear(32, 2))
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

    x = torch.randn(128, 16)
    y = torch.randint(0, 2, (128,))
    dataloader = DataLoader(TensorDataset(x, y), batch_size=8, shuffle=True)

    model, optimizer, dataloader = accelerator.prepare(model, optimizer, dataloader)

    model.train()
    for batch_x, batch_y in dataloader:
        optimizer.zero_grad()
        logits = model(batch_x)
        loss = nn.functional.cross_entropy(logits, batch_y)
        accelerator.backward(loss)
        optimizer.step()

    accelerator.print("done")

if __name__ == "__main__":
    main()
```

> Full docs: `chub get accelerate/package --lang python`

#### âœ¦ `alembic/package`

```python
# alembic/env.py
from myapp.db import Base

target_metadata = Base.metadata
```

> Full docs: `chub get alembic/package --lang python`

#### âœ¦ `aiohttp/package`

```python
import asyncio
import aiohttp

async def main() -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://httpbin.org/get") as resp:
            resp.raise_for_status()
            data = await resp.json()
            print(resp.status, data["url"])

asyncio.run(main())
```

> Full docs: `chub get aiohttp/package --lang python`

#### âœ¦ `torch/package`

```python
import torch

x = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
y = torch.tensor([[5.0, 6.0], [7.0, 8.0]])

print(x + y)
print(x @ y)
print(x.shape, x.dtype)
```

> Full docs: `chub get torch/package --lang python`

#### âœ¦ `albumentations/package`

```python
import albumentations as A

train_tf = A.Compose(
    [
        A.RandomResizedCrop(size=(224, 224), scale=(0.8, 1.0)),
        A.HorizontalFlip(p=0.5),
        A.Affine(scale=(0.9, 1.1), rotate=(-15, 15), p=0.5),
        A.Normalize(),
    ],
    strict=True,
)
```

> Full docs: `chub get albumentations/package --lang python`

#### âœ¦ `langchain/package`

```javascript
from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-4.1-mini")

response = model.invoke("Write a one-sentence summary of LangChain.")
print(response.content)
```

> Full docs: `chub get langchain/package --lang javascript`

#### âœ¦ `anthropic/package`

```javascript
from anthropic import Anthropic

client = Anthropic()

message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write a haiku about clean APIs."}
    ],
)

text = "".join(
    block.text for block in message.content if block.type == "text"
)
print(text)
```

> Full docs: `chub get anthropic/package --lang javascript`

### ðŸ¤– Agent Prompt

Copy this into your coding agent to fix all issues:

> "Fix all issues in this chub_guard report.
> For AI SDK deprecations use the recommended fix blocks above.
> For Python deprecations apply standard pyupgrade fixes.
> For JS/TS deprecations use the modern SDK patterns from chub docs.
> Do not change any logic â€” only fix deprecated patterns."

*To suppress a false positive, add `# noqa: UP<code>` to the line.*

---
## Previous Runs

- `2026-04-27 22:17:28` â€” 135 issue(s) across 24 file(s)
- `2026-04-27 22:12:55` â€” 135 issue(s) across 24 file(s)
- `2026-04-27 16:07:20` â€” 135 issue(s) across 24 file(s)
- `2026-04-27 16:06:29` â€” 135 issue(s) across 24 file(s)
- `2026-04-27 15:53:11` â€” 130 issue(s) across 23 file(s)
- `2026-04-27 15:53:09` â€” 130 issue(s) across 23 file(s)
- `2026-04-27 15:53:03` â€” 127 issue(s) across 23 file(s)
