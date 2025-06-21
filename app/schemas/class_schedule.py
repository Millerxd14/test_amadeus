from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .student import StudentInDB
from .teacher import TeacherInDB

class ClassScheduleBase(BaseModel):
    start_datetime: datetime
    end_datetime: datetime
    grade: Optional[float] = None

class ClassScheduleCreate(ClassScheduleBase):
    teacher_id: int
    student_id: int

class ClassScheduleUpdate(BaseModel):
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    grade: Optional[float] = None
    teacher_id: Optional[int] = None
    student_id: Optional[int] = None

class ClassScheduleInDB(ClassScheduleBase):
    id: int
    teacher: TeacherInDB
    student: StudentInDB

    class ConfigDict:
        from_attributes = True
