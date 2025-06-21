from typing import Optional
from .person import PersonBase

class TeacherBase(PersonBase):
    pass

class TeacherCreate(TeacherBase):
    password: str

class TeacherUpdate(PersonBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    document_number: Optional[str] = None

class TeacherInDB(TeacherBase):
    id: int

    class ConfigDict:
        from_attributes = True
