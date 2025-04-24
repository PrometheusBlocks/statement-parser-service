import os
import sys
import pytest

# Ensure project root is on sys.path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from llm.adapter import StubAdapter, get_adapter  # noqa: E402


def test_get_adapter_default(monkeypatch):
    # Default backend is stub
    monkeypatch.delenv("PARSER_BACKEND", raising=False)
    adapter = get_adapter()
    assert isinstance(adapter, StubAdapter)


def test_get_adapter_unsupported(monkeypatch):
    # Unsupported backend should raise
    monkeypatch.setenv("PARSER_BACKEND", "invalid_backend")
    with pytest.raises(ValueError) as exc:
        get_adapter()
    assert "Unsupported PARSER_BACKEND" in str(exc.value)


def test_openai_adapter_no_api_key(monkeypatch):
    # GPT-4 backend without API key should error
    monkeypatch.setenv("PARSER_BACKEND", "gpt4")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    # Attempting to load GPT-4 adapter without key may raise ValueError or ImportError
    with pytest.raises((ValueError, ImportError)):
        get_adapter()
