import os

from pydantic import ValidationError

from models.parsed_input import ParsedInput
from models.parsed_statement import ParsedStatement
from llm.adapter import get_adapter


def parse_statement(input: ParsedInput) -> ParsedStatement:
    """
    Parse a financial statement from ParsedInput pages into a ParsedStatement,
    using an LLM adapter backend.
    """
    # Concatenate all page texts
    text = os.linesep.join(page.text for page in input.pages)
    adapter = get_adapter()
    parsed = adapter.parse(text)
    # Convert parsed dict entries into Account and Transaction instances
    from data_models import Account, Transaction

    account_items = parsed.get("accounts", []) or []
    transaction_items = parsed.get("transactions", []) or []
    accounts = []
    for acct in account_items:
        accounts.append(acct if isinstance(acct, Account) else Account(**acct))
    transactions = []
    for txn in transaction_items:
        transactions.append(txn if isinstance(txn, Transaction) else Transaction(**txn))
    try:
        return ParsedStatement(
            document_id=input.document_id,
            accounts=accounts,
            transactions=transactions,
        )
    except ValidationError as e:
        raise ValueError(f"Invalid parsed statement format: {e}") from e
