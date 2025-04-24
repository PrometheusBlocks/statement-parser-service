from pydantic import BaseModel
from data_models import Account, Transaction


class ParsedStatement(BaseModel):
    document_id: str
    accounts: list[Account]
    transactions: list[Transaction]
