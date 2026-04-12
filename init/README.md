# 🛡️ chub-guard-init

**The zero-config installer for the AI-Native era.**

[![npm version](https://img.shields.io/npm/v/chub-guard-init.svg)](https://www.npmjs.com/package/chub-guard-init)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 The Problem
AI coding assistants (like Copilot, Cursor, or Gemini) often suggest project patterns that use **deprecated AI SDK APIs**. These pass your tests and standard linters but fail in production or create hidden technical debt. No existing CI tool natively catches semantic AI API deprecations because they evolve too rapidly.

## 🚀 The Solution
`chub-guard-init` is the official one-command setup for `chub-guard`. It installs a specialized git-hook that blocks modern AI project deprecations before they ever reach your codebase by syncing with live documentation.

---

## 🛠 Prerequisites

Ensure your environment is ready:
* **Node.js**: >= 18.x
* **Python**: 3.8+ (with `pip`)
* **Git**: Project must be a git repository

---

## 🏎️ Usage

Run this command once at the root of any Python project:

```bash
npx chub-guard-init
```

### What happens under the hood?
1. **Automated Hook Setup**: Installs `pre-commit` and registers the `chub-guard` linter in your `.git/hooks`.
2. **Environment Fallback**: Automatically configures the hook to work across different Python environments (virtualenvs, global, etc.) by using `python3 -m` fallbacks.
3. **Smart .gitignore**: Injects rules to ignore documentation caches (`.chub-docs/*.md`) to keep your repo light, while keeping the core linter shared with your team.
4. **Registry Injection**: Writes the initial `registry.json` mapping for common AI SDKs (OpenAI, Gemini, Anthropic, Langchain).

---

## 🏁 After Setup

Once installed, simply install the `chub` CLI to enable live documentation fetching:

```bash
npm install -g @aisuite/chub
```

Now, every time you `git commit`, the guard will proactively scan your changed files. If it finds a deprecated pattern, it will **block the commit** and provide you with a beautiful, rich terminal guide extracted directly from the official docs.

---

## ⚙️ Configuration & Maintenance

### Suppressing False Positives
If you intentionally need to keep a legacy import for a specific line, simply append the standard suppression comment:
```python
import google.generativeai as genai  # noqa: UP035
```

### Syncing with the Ecosystem
As new AI SDKs release and old ones are deprecated, keep your project in sync with the latest rules:
```bash
python scripts/chub_guard.py update-registry
```

---

## 🤝 Credits & Ecosystem
This tool is part of the **chub-guard** ecosystem and relies on **Andrew Ng’s [context-hub](https://github.com/andrewyng/context-hub)** for real-time documentation mapping.

**Documentation**: [github.com/rhealaloo45/chub-guard](https://github.com/rhealaloo45/chub-guard)

---

## 📄 License
MIT © [Rhea Laloo](https://github.com/rhealaloo45)
