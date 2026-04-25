# 🛡️ chub Deprecation Guard

**Proactive AI SDK linting that catches what standard linters miss.**

`chub-guard` automatically detects, blocks, and provides migration hints for deprecated AI SDK calls (OpenAI, Gemini, Langchain, etc.) by dynamically syncing with live documentation from the `chub` registry.

---

## 🚀 Quick Start (Recommended)

Set up the guard in any Python project with a single command using your preferred package manager:

**Using npm:**
```bash
npx chub-guard-init
```

**Using pipx:**
```bash
pipx run chub-guard-init
```

This will automatically:
* ✅ Copy the guard script and configuration.
* ✅ Install the `pre-commit` hook (handles Python path issues automatically).
* ✅ Configure your `.gitignore` to keep local doc caches out of your repo.

---

## 🧠 Why you need this
AI coding agents and LLMs frequently generate code using **deprecated SDK patterns**. These patterns pass standard linters (`ruff`, `flake8`) and type checkers (`mypy`), but cause runtime errors or technical debt.

**chub-guard catches:**
- ❌ `import google.generativeai` ➔ ✅ `from google import genai`
- ❌ `openai.ChatCompletion.create()` ➔ ✅ `client.chat.completions.create()`
- ❌ Legacy `Anthropic().completions.create()` usage
- ❌ New deprecations discovered dynamically from live docs.

---

## ✨ Features
* **Hybrid Analysis Engine**: Uses AST (Abstract Syntax Tree) for failsafe Python detection and Dynamic Markdown parsing for new deprecations from live docs.
* **Multi-Language Support**: Scans and categorizes deprecations across Python, JavaScript/TypeScript, Java, and C/C++.
* **Zero-Intervention Telemetry**: Automatically and silently syncs locally discovered patterns with the global GitHub repository via a background webhook. No developer action required!
* **Smart Registry Resolution**: Silently ignores standard library and unmapped imports, minimizing noise.
* **Rich Terminal UI**: Beautiful, color-coded error panels with exact migration code blocks extracted straight from the official docs.
* **Smart .gitignore**: Automatically manages your project's `.gitignore` to ignore documentation caches while keeping the linter shared with the team.
* **Zero Config CI**: Easily integrates into GitHub Actions to block breaking PRs.

---

## 🛠 Manual Installation
If you prefer not to use `npx`, follow these steps:

1. **Install Prerequisites**:
   ```bash
   npm install -g @aisuite/chub
   pip install pre-commit ruff rich click
   ```
2. **Add to `.pre-commit-config.yaml`**:
   ```yaml
   - repo: local
     hooks:
       - id: chub-deprecation-guard
         name: chub deprecation guard
         entry: python scripts/chub_guard.py run
         language: python
         types: [python]
   ```
3. **Run Install**:
   ```bash
   pre-commit install
   ```

---

## 🔧 Maintenance
To keep your local registry in sync with the latest AI/ML SDKs:
```bash
python scripts/chub_guard.py update-registry
```

---

## 🙏 Credits
This project is built on top of the incredible **[context-hub](https://github.com/andrewyng/context-hub)** ecosystem created by **Andrew Ng** and the DeepLearning.AI team. It uses the `chub` CLI as its primary source for real-time AI SDK documentation.

---

## 📄 License
MIT © [Rhea Laloo](https://github.com/rhealaloo45)