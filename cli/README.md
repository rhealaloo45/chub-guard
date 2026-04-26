# 🛡️ chub-guard-init (v1.2.1)

**The Universal Deprecation Guard for modern engineering teams.**

[![PyPI version](https://img.shields.io/pypi/v/chub-guard-init.svg)](https://pypi.org/project/chub-guard-init/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 The Problem
Modern development moves fast. AI coding assistants often suggest **deprecated APIs**, and browser automation tools (Selenium, Playwright) change their signatures frequently. Standard linters miss these semantic deprecations, leading to production bugs and technical debt.

## 🚀 The Solution
`chub-guard-init` is the official one-command setup for `chub-guard`. It installs a specialized git-hook that blocks deprecated patterns—from AI SDKs and Automation to Legacy Python—before they ever reach your codebase by syncing with live documentation.

---

## 🏎️ Usage

### Option 1: pipx (Recommended)
Run this command once at the root of any project:
```bash
pipx run chub-guard-init
```

### Option 2: Standard pip
```bash
pip install chub-guard-init
chub-guard-init
```

### Run on demand (Universal Scan)
Run a full project scan at any time to generate a detailed report:
```bash
chub-guard-init run-all
```
This generates a **`chub_guard_report.md`** with recommended fixes, trend lines, and Agent-ready prompts.

---

## ✨ Key Features

### 1. Hybrid Analysis (Resilient Engine)
Unlike standard linters that fail on syntax errors, `chub-guard` uses a **Resilient Regex Engine**. It will still detect critical automation and SDK deprecations even in files with Python 2/3 conflicts or broken refactors.

### 2. Polyglot Support
A single tool to guard your entire polyglot stack:
*   🐍 **Python**: Advanced AST analysis for context managers and keyword arguments.
*   🟨 **JavaScript/TypeScript**: Support for `import`, `require`, and React/Angular scoping.
*   ☕ **Java**: Package-level import detection.
*   ⚙️ **C/C++**: Header-based deprecation matching.

### 3. Rich Markdown Reporting
Generates a `chub_guard_report.md` featuring:
*   📈 **Trend Tracking**: See if your technical debt is increasing or decreasing over time.
*   🤖 **Agent-Ready Prompts**: Copy-paste prompts designed to let your AI Assistant (Cursor/Gemini) fix all issues in one go.
*   💡 **Embedded Fixes**: Exact code blocks for modern replacements, extracted directly from official docs.

### 4. Community-Powered Intelligence
*   **Live Docs**: Fetches the latest migration guides from Andrew Ng's `context-hub`.
*   **Global Sync**: Automatically stays updated with the latest community-contributed patterns from GitHub.

---

## 🧠 What does it guard?
*   **🤖 AI SDKs**: Catches breaking changes in OpenAI, Gemini, Anthropic, Langchain.
*   **🌐 Browser Automation**: Detects deprecated Selenium (`find_element_by_id`) and Playwright patterns.
*   **🐍 Legacy Code**: Identifies Python 2 syntax and legacy `urllib2`/`xrange`.
*   **🏗️ Framework Smells**: Detects architectural misconfigurations (e.g. React/Angular mixing).
*   **✨ Dynamic Docs**: Automatically flags **any** pattern marked as "deprecated" in official documentation fetched via Context-Hub.

---

## 🏁 After Setup

Every time you `git commit`, the guard will scan your changed files. If it finds a deprecated pattern, it will **block the commit** and provide a rich terminal guide extracted directly from official docs.

---

## ⚙️ Configuration

### Suppressing False Positives
Append `# noqa: CHUB` to any line:
```python
import google.generativeai as genai  # noqa: CHUB
```

### Syncing with the Ecosystem
Keep your project in sync with the latest ecosystem rules:
```bash
python scripts/chub_guard.py update-registry
```

---

## 🤝 Credits
Part of the **chub-guard** ecosystem, powered by **Andrew Ng’s [context-hub](https://github.com/andrewyng/context-hub)**.

**Full Documentation**: [github.com/rhealaloo45/chub-guard](https://github.com/rhealaloo45/chub-guard)

---

## 📄 License
MIT © [Rhea Laloo](https://github.com/rhealaloo45)
