from pydantic import BaseModel

__all__ = ["Account", "Transaction"]


class Account(BaseModel):
    """Stub Account model for statement-parser-service."""

    pass


class Transaction(BaseModel):
    """Stub Transaction model for statement-parser-service."""

    pass
