# 🛡️ Chub Guard Security & Deprecation Report
Generated on: 2026-04-27 15:36:18

## Summary: 264 issues found

### 🚩 `typing.List` is deprecated, use `list` instead
- **File:** `scripts\chub_guard.py` (Line 14)

---

### 🚩 `typing.Dict` is deprecated, use `dict` instead
- **File:** `scripts\chub_guard.py` (Line 14)

---

### 🚩 `typing.Set` is deprecated, use `set` instead
- **File:** `scripts\chub_guard.py` (Line 14)

---

### 🚩 `typing.Tuple` is deprecated, use `tuple` instead
- **File:** `scripts\chub_guard.py` (Line 14)

---

### 🚩 Use `X | None` for type annotations
- **File:** `scripts\chub_guard.py` (Line 58)

---

### 🚩 Use `X | None` for type annotations
- **File:** `scripts\chub_guard.py` (Line 59)

---

### 🚩 Use `tuple` instead of `Tuple` for type annotation
- **File:** `scripts\chub_guard.py` (Line 61)

---

### 🚩 Use `dict` instead of `Dict` for type annotation
- **File:** `scripts\chub_guard.py` (Line 61)

---

### 🚩 Use `dict` instead of `Dict` for type annotation
- **File:** `scripts\chub_guard.py` (Line 61)

---

### 🚩 Use `list` instead of `List` for type annotation
- **File:** `scripts\chub_guard.py` (Line 61)

---

### 🚩 Use `dict` instead of `Dict` for type annotation
- **File:** `scripts\chub_guard.py` (Line 77)

---

### 🚩 Use `list` instead of `List` for type annotation
- **File:** `scripts\chub_guard.py` (Line 77)

---

### 🚩 Use `tuple` instead of `Tuple` for type annotation
- **File:** `scripts\chub_guard.py` (Line 77)

---

### 🚩 Use `dict` instead of `Dict` for type annotation
- **File:** `scripts\chub_guard.py` (Line 90)

---

### 🚩 Use `list` instead of `List` for type annotation
- **File:** `scripts\chub_guard.py` (Line 90)

---

### 🚩 Use `tuple` instead of `Tuple` for type annotation
- **File:** `scripts\chub_guard.py` (Line 90)

---

### 🚩 Use `list` instead of `List` for type annotation
- **File:** `scripts\chub_guard.py` (Line 102)

---

### 🚩 Use `X | None` for type annotations
- **File:** `scripts\chub_guard.py` (Line 119)

---

### 🚩 Use `list` instead of `List` for type annotation
- **File:** `scripts\chub_guard.py` (Line 140)

---

### 🚩 Use `list` instead of `List` for type annotation
- **File:** `scripts\chub_guard.py` (Line 165)

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 50)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 54)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 56)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 60)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 62)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 67)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 68)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 71)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 74)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 76)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 84)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 87)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 88)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 89)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 90)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 91)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 92)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 100)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 105)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 106)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 107)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 108)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 109)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 113)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 131)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 134)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 136)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 140)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 141)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 142)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 149)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 150)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 151)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 152)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 153)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 154)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 155)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 156)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 157)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 158)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 160)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 162)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 163)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 164)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 165)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\main.py` (Line 166)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `error` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 13)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 47)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `error` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 117)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `error` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 120)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 120)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 123)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `error` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 153)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 155)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `error` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 226)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `error` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 334)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `error` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 437)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `openai.ChatCompletion.create` is known to be deprecated/legacy.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 491)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `OpenAI` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 492)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `from langchain.chat_models import ChatOpenAI` is known to be deprecated/legacy.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 492)

**Recommended Fix:**
```python
from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-4.1-mini")
```

---

### 🚩 `ChatCompletion` is known to be deprecated/legacy.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 533)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `OpenAI` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 538)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `error` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 606)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `error` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 623)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `error` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 635)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `error` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 666)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 805)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 824)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 826)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 950)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 952)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 969)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 984)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1004)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1047)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1068)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1078)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1161)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1171)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1173)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1179)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1188)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `error` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1228)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1239)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1369)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1376)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1387)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1388)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1389)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1403)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1430)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1431)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1451)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1477)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1478)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1503)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1504)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1529)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1530)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1534)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1535)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1536)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1551)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1560)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1561)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1567)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1765)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1766)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1775)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1788)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1789)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1792)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1816)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1832)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1835)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1837)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1842)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `error` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1861)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1893)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1894)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1896)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `cli\chub_guard_init\assets\chub_guard.py` (Line 1899)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `error` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 13)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 47)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `error` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 117)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `error` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 120)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 120)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 123)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `error` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 153)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 155)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `error` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 226)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `error` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 334)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `error` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 437)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `openai.ChatCompletion.create` is known to be deprecated/legacy.
- **File:** `init\assets\scripts\chub_guard.py` (Line 491)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `OpenAI` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 492)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `from langchain.chat_models import ChatOpenAI` is known to be deprecated/legacy.
- **File:** `init\assets\scripts\chub_guard.py` (Line 492)

**Recommended Fix:**
```python
from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-4.1-mini")
```

---

### 🚩 `ChatCompletion` is known to be deprecated/legacy.
- **File:** `init\assets\scripts\chub_guard.py` (Line 533)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `OpenAI` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 538)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `error` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 606)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `error` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 623)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `error` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 635)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `error` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 666)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 805)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 824)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 826)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 949)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 951)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 968)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 983)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1003)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1046)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1067)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1077)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1160)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1170)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1172)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1178)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1187)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `error` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1227)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1238)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1360)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1371)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1372)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1373)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1387)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1414)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1415)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1435)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1461)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1462)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1487)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1488)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1513)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1514)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1518)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1519)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1520)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1535)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1544)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1545)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1551)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1749)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1750)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1759)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1772)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1773)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1776)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1800)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1816)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1819)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1821)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1826)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `error` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1845)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1877)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1878)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1880)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `init\assets\scripts\chub_guard.py` (Line 1883)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `error` is deprecated.
- **File:** `scripts\chub_guard.py` (Line 11)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `error` is deprecated.
- **File:** `scripts\chub_guard.py` (Line 79)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `error` is deprecated.
- **File:** `scripts\chub_guard.py` (Line 92)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `error` is deprecated.
- **File:** `scripts\chub_guard.py` (Line 105)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `error` is deprecated.
- **File:** `scripts\chub_guard.py` (Line 121)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `error` is deprecated.
- **File:** `scripts\chub_guard.py` (Line 144)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `error` is deprecated.
- **File:** `scripts\chub_guard.py` (Line 223)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `print` is deprecated.
- **File:** `scripts\chub_guard.py` (Line 245)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `scripts\chub_guard.py` (Line 250)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `scripts\chub_guard.py` (Line 252)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `scripts\chub_guard.py` (Line 254)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `google.generativeai` is known to be deprecated/legacy.
- **File:** `tests\test_app.py` (Line 1)

---

### 🚩 `import google.generativeai` is known to be deprecated/legacy.
- **File:** `tests\test_app.py` (Line 1)

---

### 🚩 `CliRunner` is deprecated.
- **File:** `tests\test_chub_guard.py` (Line 7)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `CliRunner` is deprecated.
- **File:** `tests\test_chub_guard.py` (Line 13)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `google.generativeai` is known to be deprecated/legacy.
- **File:** `tests\test_chub_guard.py` (Line 19)

---

### 🚩 `google.generativeai` is known to be deprecated/legacy.
- **File:** `tests\test_chub_guard.py` (Line 54)

---

### 🚩 `import google.generativeai` is known to be deprecated/legacy.
- **File:** `tests\test_chub_guard.py` (Line 54)

---

### 🚩 `google.generativeai` is known to be deprecated/legacy.
- **File:** `tests\test_chub_guard.py` (Line 60)

---

### 🚩 `import google.generativeai` is known to be deprecated/legacy.
- **File:** `tests\test_chub_guard.py` (Line 60)

---

### 🚩 `openai.ChatCompletion.create` is known to be deprecated/legacy.
- **File:** `tests\test_chub_guard.py` (Line 76)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `print` is deprecated.
- **File:** `tests\test_chub_guard.py` (Line 121)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `tests\test_chub_guard.py` (Line 149)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `google.generativeai` is known to be deprecated/legacy.
- **File:** `tests\test_chub_guard.py` (Line 194)

---

### 🚩 `google.generativeai` is known to be deprecated/legacy.
- **File:** `tests\test_chub_guard.py` (Line 195)

---

### 🚩 `error` is deprecated.
- **File:** `tests\test_chub_guard.py` (Line 207)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `error` is deprecated.
- **File:** `tests\test_chub_guard.py` (Line 214)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `google.generativeai` is known to be deprecated/legacy.
- **File:** `tests\test_py_gaps.py` (Line 2)

---

### 🚩 `import google.generativeai` is known to be deprecated/legacy.
- **File:** `tests\test_py_gaps.py` (Line 2)

---

### 🚩 `openai.ChatCompletion.create` is known to be deprecated/legacy.
- **File:** `tests\test_py_gaps.py` (Line 6)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `ChatCompletion` is known to be deprecated/legacy.
- **File:** `tests\test_py_gaps.py` (Line 8)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `ChatCompletion` is known to be deprecated/legacy.
- **File:** `tests\test_py_gaps.py` (Line 9)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 aiohttp.ClientSession() should be used with `async with`.
- **File:** `tests\test_registry_py.py` (Line 31)

---

### 🚩 `print` is deprecated.
- **File:** `tests\test_registry_py.py` (Line 34)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `tests\test_registry_py.py` (Line 66)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `print` is deprecated.
- **File:** `tests\test_registry_py.py` (Line 77)

**Recommended Fix:**
```python
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, show_default=True, type=int)
def cli(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

---

### 🚩 `OpenAI` is deprecated according to chub docs.
- **File:** `tests\test_app.js` (Line 2)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `ChatCompletion` is known to be deprecated/legacy.
- **File:** `tests\test_app.js` (Line 1)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `OpenAI` is deprecated according to chub docs.
- **File:** `tests\test_js_gaps.js` (Line 2)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `ChatCompletion` is known to be deprecated/legacy.
- **File:** `tests\test_js_gaps.js` (Line 10)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `openai.ChatCompletion.create` is known to be deprecated/legacy.
- **File:** `tests\test_pip.js` (Line 9)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `text-davinci-003` is known to be deprecated/legacy.
- **File:** `tests\test_pip.js` (Line 10)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `claude-2` is known to be deprecated/legacy.
- **File:** `tests\test_pip.js` (Line 17)

---

### 🚩 `AI_PROMPT` is known to be deprecated/legacy.
- **File:** `tests\test_pip.js` (Line 18)

---

### 🚩 `HUMAN_PROMPT` is known to be deprecated/legacy.
- **File:** `tests\test_pip.js` (Line 18)

---

### 🚩 `OpenAI` is deprecated according to chub docs.
- **File:** `tests\test_react.jsx` (Line 2)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---

### 🚩 `ChatCompletion` is known to be deprecated/legacy.
- **File:** `tests\test_react.jsx` (Line 7)

**Recommended Fix:**
```python
from openai import OpenAI

client = OpenAI()
```

---
