import os
import json
import abc


class BaseAdapter(abc.ABC):
    @abc.abstractmethod
    def parse(self, text: str) -> dict:
        """Parse statement text into JSON dict with accounts and transactions."""
        pass


class StubAdapter(BaseAdapter):
    def parse(self, text: str) -> dict:
        """Return a fixed stubbed response."""
        return {"accounts": [{}], "transactions": []}


class OpenAIAdapter(BaseAdapter):
    def __init__(self):
        try:
            import openai
        except ImportError:
            raise ImportError("openai package is required for OpenAIAdapter")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY must be set for OpenAIAdapter")
        openai.api_key = api_key
        self.openai = openai

    def parse(self, text: str) -> dict:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a finance statement parser. Parse the provided statement "
                    "text and output only valid JSON with keys 'accounts' (list of accounts) "
                    "and 'transactions' (list of transactions)."
                ),
            },
            {"role": "user", "content": text},
        ]
        response = self.openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            temperature=0,
        )
        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError("Failed to parse JSON from OpenAI response") from e


def get_adapter() -> BaseAdapter:
    """Instantiate adapter based on PARSER_BACKEND environment variable."""
    backend = os.getenv("PARSER_BACKEND", "stub").lower()
    if backend == "stub":
        return StubAdapter()
    if backend == "gpt4":
        return OpenAIAdapter()
    raise ValueError(f"Unsupported PARSER_BACKEND: {backend}")
