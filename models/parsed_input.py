from pydantic import BaseModel


class Page(BaseModel):
    number: int
    text: str


class ParsedInput(BaseModel):
    document_id: str
    pages: list[Page]
