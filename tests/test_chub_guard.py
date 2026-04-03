import json
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from click.testing import CliRunner

from scripts.chub_guard import cli, extract_chub_hint, REPO_ROOT, REGISTRY_PATH

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def mock_registry(tmp_path):
    registry_file = tmp_path / "registry.json"
    registry_data = {
        "google.generativeai": "gemini/genai",
        "openai": "openai/openai"
    }
    registry_file.write_text(json.dumps(registry_data))
    return registry_file

def test_no_python_files(runner, tmp_path):
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("hello")
    result = runner.invoke(cli, ["run", str(txt_file)])
    assert result.exit_code == 0

@patch("scripts.chub_guard.subprocess.run")
@patch("scripts.chub_guard.shutil.which", return_value="chub")
@patch("scripts.chub_guard.REGISTRY_PATH")
def test_clean_file_passes(mock_registry_path, mock_which, mock_run, runner, tmp_path, mock_registry):
    mock_registry_path.read_text.return_value = mock_registry.read_text()
    
    # Mock ruff output
    mock_run.return_value = MagicMock(stdout="[]", returncode=0)
    
    py_file = tmp_path / "test_clean.py"
    py_file.write_text("from google import genai\nclient = genai.Client()")
    
    result = runner.invoke(cli, ["run", str(py_file)])
    assert result.exit_code == 0
    assert "✓ No deprecated API calls detected" in result.output

@patch("scripts.chub_guard.subprocess.run")
@patch("scripts.chub_guard.shutil.which", return_value="chub")
@patch("scripts.chub_guard.REGISTRY_PATH")
def test_deprecated_import_caught(mock_registry_path, mock_which, mock_run, runner, tmp_path, mock_registry):
    mock_registry_path.read_text.return_value = mock_registry.read_text()
    
    py_file = tmp_path / "test_deprecated.py"
    py_file.write_text("import google.generativeai as genai")
    
    ruff_output = json.dumps([{
        "filename": str(py_file),
        "location": {"row": 1, "column": 1},
        "code": "UP035",
        "message": "`import google.generativeai` is deprecated"
    }])
    mock_run.return_value = MagicMock(stdout=ruff_output, returncode=0)
    
    result = runner.invoke(cli, ["run", str(py_file)])
    assert result.exit_code == 1
    assert "✗ DEPRECATED API DETECTED" in result.output
    assert "UP035" in result.output

@patch("scripts.chub_guard.subprocess.run")
@patch("scripts.chub_guard.shutil.which", return_value="chub")
@patch("scripts.chub_guard.REGISTRY_PATH")
def test_openai_deprecated_caught(mock_registry_path, mock_which, mock_run, runner, tmp_path, mock_registry):
    mock_registry_path.read_text.return_value = mock_registry.read_text()
    
    py_file = tmp_path / "test_openai.py"
    py_file.write_text("import openai\nopenai.ChatCompletion.create()")
    
    ruff_output = json.dumps([{
        "filename": str(py_file),
        "location": {"row": 2, "column": 1},
        "code": "UP035",
        "message": "deprecated call"
    }])
    mock_run.return_value = MagicMock(stdout=ruff_output, returncode=0)
    
    result = runner.invoke(cli, ["run", str(py_file)])
    assert result.exit_code == 1
    assert "✗ DEPRECATED API DETECTED" in result.output

@patch("scripts.chub_guard.subprocess.run")
@patch("scripts.chub_guard.shutil.which")
@patch("scripts.chub_guard.REGISTRY_PATH")
def test_chub_unavailable_no_block(mock_registry_path, mock_which, mock_run, runner, tmp_path, mock_registry):
    mock_registry_path.read_text.return_value = mock_registry.read_text()
    
    def side_effect(cmd):
        if cmd == "chub":
            return None
        return "ruff"
    mock_which.side_effect = side_effect
    
    py_file = tmp_path / "test_clean.py"
    py_file.write_text("from google import genai")
    
    mock_run.return_value = MagicMock(stdout="[]", returncode=0)
    
    result = runner.invoke(cli, ["run", str(py_file)])
    assert result.exit_code == 0
    assert "⚠ chub unavailable" in result.output

@patch("scripts.chub_guard.subprocess.run")
@patch("scripts.chub_guard.shutil.which", return_value="chub")
@patch("scripts.chub_guard.REGISTRY_PATH")
@patch("scripts.chub_guard.DOCS_DIR")
def test_cache_used_within_24h(mock_docs_dir, mock_registry_path, mock_which, mock_run, runner, tmp_path, mock_registry):
    mock_registry_path.read_text.return_value = mock_registry.read_text()
    
    # Setup mock doc cache
    safe_name = "gemini__genai"
    doc_path = tmp_path / f"{safe_name}.md"
    doc_path.write_text("## Usage\n```python\nprint('hi')\n```")
    
    mock_docs_dir.__truediv__.return_value = doc_path
    
    py_file = tmp_path / "test_clean.py"
    py_file.write_text("import my_sdk")
    
    registry_data = json.loads(mock_registry.read_text())
    registry_data["my_sdk"] = "gemini/genai"
    mock_registry_path.read_text.return_value = json.dumps(registry_data)
    
    mock_run.return_value = MagicMock(stdout="[]", returncode=0)
    
    result = runner.invoke(cli, ["run", str(py_file)])
    assert result.exit_code == 0
    # chub should not be called
    for call in mock_run.call_args_list:
        assert "chub" not in call.args[0]

@patch("scripts.chub_guard.subprocess.run")
@patch("scripts.chub_guard.shutil.which", return_value="chub")
@patch("scripts.chub_guard.REGISTRY_PATH")
@patch("scripts.chub_guard.DOCS_DIR")
def test_cache_refreshed_after_24h(mock_docs_dir, mock_registry_path, mock_which, mock_run, runner, tmp_path, mock_registry):
    mock_registry_path.read_text.return_value = mock_registry.read_text()
    
    safe_name = "gemini__genai"
    doc_path = tmp_path / f"{safe_name}.md"
    doc_path.write_text("## Usage\n```python\nprint('hi')\n```")
    
    # Set modify time to 25 hours ago
    past_time = time.time() - (25 * 3600)
    import os
    os.utime(doc_path, (past_time, past_time))
    
    mock_docs_dir.__truediv__.return_value = doc_path
    
    py_file = tmp_path / "test_clean.py"
    py_file.write_text("import my_sdk")
    
    registry_data = json.loads(mock_registry.read_text())
    registry_data["my_sdk"] = "gemini/genai"
    mock_registry_path.read_text.return_value = json.dumps(registry_data)
    
    mock_run.return_value = MagicMock(stdout="[]", returncode=0)
    
    result = runner.invoke(cli, ["run", str(py_file)])
    assert result.exit_code == 0
    
    # chub SHOULD be called
    chub_called = any("chub" in call.args[0] for call in mock_run.call_args_list)
    assert chub_called

@patch("scripts.chub_guard.subprocess.run")
@patch("scripts.chub_guard.shutil.which", return_value="chub")
@patch("scripts.chub_guard.REGISTRY_PATH")
def test_noqa_suppression(mock_registry_path, mock_which, mock_run, runner, tmp_path, mock_registry):
    mock_registry_path.read_text.return_value = mock_registry.read_text()
    
    py_file = tmp_path / "test_noqa.py"
    py_file.write_text("import google.generativeai  # noqa: UP035")
    
    # Mock ruff output empty because noqa suppressed it
    mock_run.return_value = MagicMock(stdout="[]", returncode=0)
    
    result = runner.invoke(cli, ["run", str(py_file)])
    assert result.exit_code == 0

def test_registry_maps_correctly():
    registry_file = REGISTRY_PATH
    if not registry_file.exists():
        pytest.skip("registry.json not created yet")
    registry = json.loads(registry_file.read_text())
    assert "google.generativeai" in registry
    assert registry["google.generativeai"] == "gemini/genai"
    for k, v in registry.items():
        assert isinstance(k, str)
        assert isinstance(v, str)
        assert "/" in v

@patch("scripts.chub_guard.subprocess.run")
@patch("scripts.chub_guard.shutil.which", return_value="chub")
@patch("scripts.chub_guard.REGISTRY_PATH")
def test_ast_parse_failure_skipped(mock_registry_path, mock_which, mock_run, runner, tmp_path, mock_registry):
    mock_registry_path.read_text.return_value = mock_registry.read_text()
    
    py_file = tmp_path / "test_syntax_error.py"
    py_file.write_text("def class return:") # invalid syntax
    
    mock_run.return_value = MagicMock(stdout="[]", returncode=0)
    
    result = runner.invoke(cli, ["run", str(py_file)])
    assert result.exit_code == 0
    assert "Warning: Syntax error" in result.output
