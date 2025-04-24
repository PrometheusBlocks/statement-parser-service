import os
import sys

# Ensure project root is on sys.path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.parsed_input import ParsedInput, Page  # noqa: E402
from service.core import parse_statement  # noqa: E402
from llm.adapter import StubAdapter  # noqa: E402


def test_parse_statement_with_stub(monkeypatch):
    # Ensure stub adapter is used
    monkeypatch.setenv("PARSER_BACKEND", "stub")
    # Monkey-patch get_adapter to return StubAdapter explicitly
    import llm.adapter as adapter_module

    monkeypatch.setattr(adapter_module, "get_adapter", lambda: StubAdapter())

    dummy_input = ParsedInput(
        document_id="doc123",
        pages=[Page(number=1, text="dummy text")],
    )
    result = parse_statement(dummy_input)
    # Check instance types and content
    from data_models import Account

    assert result.document_id == "doc123"
    assert isinstance(result.accounts, list)
    assert len(result.accounts) >= 1
    assert isinstance(result.accounts[0], Account)
    assert isinstance(result.transactions, list)
    # transactions list may be empty or stubbed
    for txn in result.transactions:
        from data_models import Transaction

        assert isinstance(txn, Transaction)
