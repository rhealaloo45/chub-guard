# chub Deprecation Guard

A proactive `pre-commit` and CI linting tool that automatically detects, blocks, and provides migration hints for deprecated AI SDK API calls in Python codebases by dynamically syncing with live documentation from the [chub CLI](https://npmjs.com/package/@aisuite/chub).

## The Problem
AI coding agents (like Copilot, Claude, or Gemini) and outdated StackOverflow snippets frequently generate syntactically valid Python code using deprecated SDK APIs. For example:
- `import google.generativeai` instead of `from google import genai`
- `openai.ChatCompletion.create()` instead of `client.chat.completions.create()`
- Legacy `MistralClient` instead of `Mistral`

These pass all standard linters (`ruff`, `flake8`) and type checkers (`mypy`), compile cleanly, but fail silently or noisily in production. No existing CI tool natively catches semantic AI API deprecations because they evolve too rapidly.

## The Solution
The **chub Deprecation Guard** hooks into your Git workflow to:
1. Parse your staged Python files.
2. Fetch the latest, versioned usage docs for any detected AI SDKs directly from `chub` (e.g., OpenAI, Langchain, Anthropic, Gemini).
3. Dynamically scan the official documentation for keywords like "deprecated", "legacy", or "incorrect".
4. Run `ruff` (with the `UP` pyupgrade rule) and augment any violations with the exact replacement code block extracted straight from the `chub` markdown.
5. Block the commit with a rich terminal UI if deprecated patterns are found.

## Installation

1. **Install the chub CLI globally** (Required to fetch live docs)
   ```bash
   npm install -g @aisuite/chub
   ```

2. **Install Python dependencies**
   ```bash
   pip install pre-commit ruff rich click
   ```

3. **Install the pre-commit hook**
   Add this block to your `.pre-commit-config.yaml` at the root of your repository:
   ```yaml
   repos:
     - repo: local
       hooks:
         - id: chub-deprecation-guard
           name: chub deprecation guard
           entry: python scripts/chub_guard.py run
           language: python
           types: [python]
           pass_filenames: true
           stages: [pre-commit]
           additional_dependencies:
             - rich
             - click
             - ruff
   ```
   Then run:
   ```bash
   pre-commit install
   ```

## Usage

Once installed, the guard runs automatically every time you run `git commit`. 

If you attempt to commit a file containing a deprecated AI SDK pattern, the commit will be blocked, and you will see a detailed error message displaying the correct, modern API usage directly from the framework's documentation.

### Suppressing False Positives
If you intentionally need to maintain a legacy script and want to bypass the guard for a specific line, simply append a `# noqa: UP035` comment to the end of the line:
```python
import google.generativeai as genai  # noqa: UP035
```

### Manual Scanning
You can manually run the scanner across your entire codebase without triggering a commit:
```bash
pre-commit run chub-deprecation-guard --all-files
```

## Running in CI (GitHub Actions)
The tool is built to run flawlessly in CI pipelines. See `.github/workflows/chub-guard.yml` for an example of how to run this on every Pull Request.

## Architecture & Internals
For an in-depth look at how the hybrid AST and dynamic markdown parsing engine works, please see the [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) document.