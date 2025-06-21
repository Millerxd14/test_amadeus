from pydantic import BaseModel

class PersonBase(BaseModel):
    first_name: str
    last_name: str
    age: int
    document_number: str
