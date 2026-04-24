# 🛡️ Chub Guard Report

## 🕐 Run: 2026-04-24 06:54:30

**4** issues found across **1** file.

*Trend: ↓ 3 fewer than last run*

### ✦ AI SDK Deprecations

| # | File | Line | Severity | Issue |
|---|------|------|----------|-------|
| 1 | `tests/test_py_gaps.py` | 2 | 🔴 Breaking | `google.generativeai` is flagged as deprecated or incorrect by chub docs. *[gemini/genai]* |
| 2 | `tests/test_py_gaps.py` | 6 | 🔴 Breaking | `ChatCompletion` is flagged as deprecated or incorrect by chub docs. *[openai/package]* |
| 3 | `tests/test_py_gaps.py` | 8 | 🔴 Breaking | `ChatCompletion` is flagged as deprecated or incorrect by chub docs. *[openai/package]* |
| 4 | `tests/test_py_gaps.py` | 9 | 🔴 Breaking | `ChatCompletion` is flagged as deprecated or incorrect by chub docs. *[openai/package]* |


### Recommended Fixes

#### ✦ `gemini/genai`

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

- `2026-04-24 06:44:47` — 7 issue(s) across 1 file(s)
- `2026-04-24 06:43:49` — 4 issue(s) across 1 file(s)
- `2026-04-24 06:22:41` — 4 issue(s) across 1 file(s)
- `2026-04-24 06:22:12` — 4 issue(s) across 1 file(s)
- `2026-04-24 06:13:11` — 3 issue(s) across 1 file(s)
- `2026-04-24 06:10:58` — 7 issue(s) across 1 file(s)
- `2026-04-24 06:04:26` — 2 issue(s) across 1 file(s)
- `2026-04-24 06:02:49` — 2 issue(s) across 1 file(s)
- `2026-04-23 09:38:40` — 3 issue(s) across 1 file(s)
- `2026-04-23 09:37:12` — 2 issue(s) across 1 file(s)
- `2026-04-23 09:35:02` — 5 issue(s) across 1 file(s)
- `2026-04-23 09:08:48` — 2 issue(s) across 1 file(s)
- `2026-04-23 09:04:03` — 2 issue(s) across 1 file(s)
- `2026-04-23 09:00:56` — 1 issue(s) across 1 file(s)
- `2026-04-23 08:59:12` — 1 issue(s) across 1 file(s)
- `2026-04-23 07:33:26` — 2 issue(s) across 1 file(s)
- `2026-04-23 07:29:40` — 1 issue(s) across 1 file(s)
- `2026-04-23 07:24:37` — 1 issue(s) across 1 file(s)
- `2026-04-23 07:22:06` — 3 issue(s) across 2 file(s)
- `2026-04-23 07:21:29` — 1 issue(s) across 1 file(s)
- `2026-04-23 07:21:14` — 2 issue(s) across 1 file(s)
- `2026-04-23 07:20:59` — 1 issue(s) across 1 file(s)
- `2026-04-23 07:19:22` — 1 issue(s) across 1 file(s)
- `2026-04-23 07:18:42` — 1 issue(s) across 1 file(s)
- `2026-04-23 07:00:53` — 2 issue(s) across 1 file(s)
- `2026-04-23 06:56:06` — 2 issue(s) across 1 file(s)
- `2026-04-23 06:54:50` — 1 issue(s) across 1 file(s)
- `2026-04-23 06:51:07` — 1 issue(s) across 1 file(s)
- `2026-04-21 09:39:36` — 1 issue(s) across 1 file(s)
- `2026-04-21 09:32:36` — 1 issue(s) across 1 file(s)
- `2026-04-21 07:54:17` — 1 issue(s) across 1 file(s)
- `2026-04-21 07:47:09` — 4 issue(s) across 2 file(s)
- `2026-04-21 07:45:48` — 1 issue(s) across 1 file(s)
- `2026-04-21 07:28:09` — 3 issue(s) across 1 file(s)
- `2026-04-21 07:27:27` — 3 issue(s) across 1 file(s)
- `2026-04-21 07:26:49` — 3 issue(s) across 1 file(s)
