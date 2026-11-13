"""The current-usage rule: nothing a doc's own current examples use is flagged as deprecated.

Before this, any name mentioned near a warning word was read as deprecated, so advice about how to use
a current call ("Do not treat `message.content` as a single string") flagged the call itself.
"""
import importlib
from pathlib import Path

import pytest

import scripts.chub_guard as cg

DOC = "\n".join([
    "# Anthropic",
    "## Usage",
    "```python",
    'message = client.messages.create(model="claude-sonnet-4-5", max_tokens=64, messages=[])',
    "print(message.content[0].text)",
    "```",
    "- Do not treat `message.content` as a single string.",
    "- Do not use the following deprecated models (or their variants like",
    "  `claude-2.1`):",
    "- Legacy: `client.completions.create` is deprecated.",
])


def test_current_usage_counts_examples_not_warnings():
    use = cg._current_usage(DOC)
    assert "message.content" in use                      # used in the example code
    assert "claude-2.1" not in use                       # named on the second line of a warning
    assert "client.completions.create" not in use        # deprecated


def test_drop_current_removes_used_patterns_and_bare_versions():
    use = cg._current_usage(DOC)
    kept = cg._drop_current(["message.content", "client.completions.create", "claude-2.1", "1.2.11"], use)
    assert kept == ["client.completions.create", "claude-2.1"]


def test_word_in_matches_whole_identifiers():
    assert cg._word_in("create", "client.chat.completions.create({})")
    assert not cg._word_in("create", "const createdAt = 1")
    assert not cg._word_in("OpenAI", "const x = new OpenAIClient()")


def test_legacy_switch_runs_the_old_rules(monkeypatch):
    monkeypatch.setattr(cg, "LEGACY_RULES", True)
    assert cg._drop_current(["message.content", "1.2.11"], cg._current_usage(DOC)) == ["message.content", "1.2.11"]


def test_js_current_code_is_not_flagged(tmp_path):
    registry = {"openai": "openai/package"}
    patterns = {"openai/package": ["openai.ChatCompletion.create", "client.chat.completions.create"]}
    modern = tmp_path / "modern.js"
    modern.write_text('import OpenAI from "openai";\nconst client = new OpenAI();\n'
                      'const r = await client.chat.completions.create({});\n')
    use = {"openai/package": 'client.chat.completions.create\nfrom openai import OpenAI'}
    patterns = {k: cg._drop_current(v, use[k]) for k, v in patterns.items()}
    assert [v for v in cg.analyze_js_file(modern, registry, patterns) if "deprecated" in v["message"]] == []
    old = tmp_path / "old.js"
    old.write_text('import OpenAI from "openai";\nconst r = await openai.ChatCompletion.create({});\n')
    assert any("ChatCompletion" in v["message"] for v in cg.analyze_js_file(old, registry, patterns))
