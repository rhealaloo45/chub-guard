# 🛡️ chub Deprecation Guard (v1.2.1)

**Universal project linting that catches what standard tools miss.**

`chub-guard` is a polyglot, resilient deprecation guard that automatically detects, blocks, and provides migration hints for **everything** from AI SDKs and Browser Automation to Legacy Python patterns. It dynamically syncs with live documentation from the `chub` registry to provide the most up-to-date engineering safety net.

---

## 🚀 Quick Start (Recommended)

The fastest way to use `chub-guard` is through the **VS Code Extension**, which provides real-time, "as-you-type" feedback.

### 1. Install via VS Code (Easiest)
Search for **`chub-guard`** in the VS Code Marketplace. Upon activation, it will automatically detect and set up the guard for your project.

### 2. Manual CLI Setup
Alternatively, set up the guard manually in any Python or JS project:

**Using npm:**
```bash
npx chub-guard-init
```

**Using pipx:**
```bash
pipx run chub-guard-init
```

**Run on demand (Project-wide scan & report):**
```bash
# Get a beautiful markdown report with trend lines and AI fixes
npx chub-guard-init run-all
```

---

## 🧠 Not Just for AI SDKs: A Universal Safety Net
Standard linters (`ruff`, `eslint`) are great for syntax, but they can't keep up with rapidly evolving APIs and browser automation tools. `chub-guard` fills this gap by acting as a **Universal Guard** for:

*   **🤖 AI SDKs**: Catches breaking changes in OpenAI, Gemini, Anthropic, Langchain, etc.
*   **🌐 Browser Automation**: Detects deprecated Selenium (`find_element_by_id`) and Playwright (`waitForSelector`) patterns.
*   **🐍 Legacy Code**: Identifies Python 2 syntax, legacy `urllib2`, and `xrange` in modern projects.
*   **🏗️ Framework Smells**: Detects architectural misconfigurations, like mixing Angular and React imports in the same file.
*   **✨ Dynamic Docs**: Automatically flags **any** pattern marked as "deprecated" or "legacy" in official documentation fetched via Context-Hub.

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

## 🔧 Maintenance
To keep your local project in sync with the latest ecosystem releases:
```bash
python scripts/chub_guard.py update-registry
```

---

## 🙏 Credits
This project is built on top of the incredible **[context-hub](https://github.com/andrewyng/context-hub)** ecosystem created by **Andrew Ng** and the DeepLearning.AI team.

---

## 📄 License
MIT © [Rhea Laloo](https://github.com/rhealaloo45)