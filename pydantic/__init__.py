"""
Stub pydantic package for statement-parser-service.
"""


class ValidationError(Exception):
    """Stub ValidationError."""

    pass


class BaseModel:
    """Stub BaseModel to accept any fields without validation."""

    def __init__(self, **data):
        for key, value in data.items():
            setattr(self, key, value)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.__dict__)
