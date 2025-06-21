from typing import Optional
from .person import PersonBase
from pydantic import BaseModel

class StudentBase(PersonBase):
    pass

class StudentCreate(StudentBase):
    password: str

class StudentUpdate(PersonBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    document_number: Optional[str] = None

class StudentInDB(StudentBase):
    id: int

    class ConfigDict:
        from_attributes = True
