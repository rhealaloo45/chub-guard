# 🛡️ Chub Guard Report

## 🕐 Run: 2026-04-23 09:38:40

**3** issues found across **1** file.

*Trend: ↑ 1 more than last run*

### 🟨 JS/TS Deprecations (Chub)

| # | File | Line | Severity | Issue |
|---|------|------|----------|-------|
| 1 | `tests/test_registry_react.js` | 2 | 🔴 Breaking | `React` is deprecated (from pattern: `import React from "react"`). See chub docs. *[react/react]* |
| 2 | `tests/test_registry_react.js` | 19 | 🔴 Breaking | `import React from "react"` is flagged as deprecated by chub docs. *[react/react]* |
| 3 | `tests/test_registry_react.js` | 22 | 🔴 Breaking | `React` is deprecated (from pattern: `import React from "react"`). See chub docs. *[react/react]* |


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
