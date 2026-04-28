# ðŸ›¡ï¸ Chub Guard Report

## ðŸ• Run: 2026-04-27 18:21:29

**4** issues found across **1** file.

### ðŸ›¡ï¸ Upgrade Readiness
Your project was scanned against the **LATEST** documentation from Context-Hub to ensure you are aware of upcoming deprecations and migration paths.

### ðŸ“¦ Local Environment
The following versions are currently installed/pinned in your project:
- (No pinned versions detected, using latest documentation)

*Trend: â†“ 100 fewer than last run*

### âœ¦ AI SDK Deprecations

| # | File | Line | Severity | Issue |
|---|------|------|----------|-------|
| 1 | `test_deprecations.py` | 1 | ðŸŸ¡ Warning | Legacy Python 2 `print` statement detected. Use `print()` function. |
| 2 | `test_deprecations.py` | 2 | ðŸ”´ Breaking | `urllib2` is deprecated/removed in Python 3. Use `urllib.request` or `requests`. *[python/urllib2]* |
| 3 | `test_deprecations.py` | 5 | ðŸ”´ Breaking | Deprecated Selenium locator method. Use `find_element(By.ID, ...)` syntax. *[selenium/package]* |

### ðŸ Python Deprecations & Issues

| # | File | Line | Code | Issue |
|---|------|------|------|-------|
| 1 | `test_deprecations.py` | 1 | `invalid-syntax` | Simple statements must be separated by newlines or semicolons |


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
