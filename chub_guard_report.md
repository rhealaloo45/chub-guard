# 🛡️ Chub Guard Report

## 🕐 Run: 2026-04-24 10:08:18

**7** issues found across **1** file.

*Trend: ↑ 3 more than last run*

### ✦ AI SDK Deprecations

| # | File | Line | Severity | Issue |
|---|------|------|----------|-------|
| 1 | `tests/test_registry_py.py` | 7 | 🔴 Breaking | Argument `fp16=True` is deprecated in `Accelerator`. Use `mixed_precision='fp16'` instead. *[accelerate/package]* |
| 2 | `tests/test_registry_py.py` | 31 | 🔵 Info | aiohttp.ClientSession() should be used with `async with` to ensure proper connection pooling and cleanup. *[aiohttp/package]* |
| 3 | `tests/test_registry_py.py` | 28 | 🔴 Breaking | `async` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 4 | `tests/test_registry_py.py` | 30 | 🔴 Breaking | `async` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 5 | `tests/test_registry_py.py` | 31 | 🔴 Breaking | `async` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |
| 6 | `tests/test_registry_py.py` | 33 | 🔴 Breaking | `resp.text` is flagged as deprecated or incorrect by chub docs. *[aiohttp/package]* |
| 7 | `tests/test_registry_py.py` | 37 | 🔴 Breaking | `async` is flagged as deprecated or incorrect by chub docs. *[alembic/package]* |


### Recommended Fixes

#### ✦ `accelerate/package`

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

#### ✦ `aiohttp/package`

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

#### ✦ `alembic/package`

```python
# alembic/env.py
from myapp.db import Base

target_metadata = Base.metadata
```

> Full docs: `chub get alembic/package --lang python`

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

- `2026-04-24 06:54:30` — 4 issue(s) across 1 file(s)
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
