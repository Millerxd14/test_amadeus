from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    kind : str | None = None

class TokenData(BaseModel):
    document_number: str | None = None
