# 🛡️ Chub Guard Report

## 🕒 Run: 2026-04-30 06:26:20

**2** issues found across **1** file.

### 🛡️ Upgrade Readiness
Your project was scanned against the **LATEST** documentation from Context-Hub to ensure you are aware of upcoming deprecations and migration paths.

### 📦 Local Environment
The following versions are currently installed/pinned in your project:
- (No pinned versions detected, using latest documentation)

*Trend: ↑ 1 more than last run*

### ✦ AI SDK Deprecations

| # | File | Line | Severity | Issue |
|---|------|------|----------|-------|
| 1 | `C:/Users/Rhea/AppData/Local/Temp/pytest-of-Rhea/pytest-0/test_openai_deprecated_caught0/test_openai.py` | 2 | 🔴 Breaking | `ChatCompletion.create` is flagged as deprecated or incorrect by chub docs. *[openai/package]* |

### 🐍 Python Deprecations & Issues

| # | File | Line | Code | Issue |
|---|------|------|------|-------|
| 1 | `C:/Users/Rhea/AppData/Local/Temp/pytest-of-Rhea/pytest-0/test_openai_deprecated_caught0/test_openai.py` | 2 | `UP035` | deprecated call |


### Recommended Fixes

#### ✦ `openai/package`

```python
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

> Full docs: `chub get openai/package --lang python`

### 🤖 Agent Prompt

Copy this into your coding agent to fix all issues:

> "Fix all issues in this chub_guard report.
> For AI SDK deprecations use the recommended fix blocks above.
> For Python deprecations apply standard pyupgrade fixes.
> For JS/TS deprecations use the modern SDK patterns from chub docs.
> Do not change any logic — only fix deprecated patterns."

*To suppress a false positive, add `# noqa: UP<code>` to the line.*

---
## Previous Runs

- `2026-04-30 06:26:19` — 1 issue(s) across 1 file(s)
- `2026-04-27 18:18:05` â€” 104 issue(s) across 23 file(s)
- `2026-04-27 18:14:14` â€” 120 issue(s) across 24 file(s)
- `2026-04-27 18:10:54` â€” 120 issue(s) across 24 file(s)
- `2026-04-27 22:19:57` â€” 135 issue(s) across 24 file(s)
- `2026-04-27 22:17:28` â€” 135 issue(s) across 24 file(s)
- `2026-04-27 22:12:55` â€” 135 issue(s) across 24 file(s)
- `2026-04-27 16:07:20` â€” 135 issue(s) across 24 file(s)
- `2026-04-27 16:06:29` â€” 135 issue(s) across 24 file(s)
- `2026-04-27 15:53:11` â€” 130 issue(s) across 23 file(s)
- `2026-04-27 15:53:09` â€” 130 issue(s) across 23 file(s)
- `2026-04-27 15:53:03` â€” 127 issue(s) across 23 file(s)
