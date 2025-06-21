from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database.connection import Base

class ClassSchedule(Base):
    __tablename__ = "class_schedules"

    id = Column(Integer, primary_key=True, index=True)
    start_datetime = Column(DateTime, index=True)
    end_datetime = Column(DateTime, index=True)
    grade = Column(Float, nullable=True)

    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    student_id = Column(Integer, ForeignKey("students.id"))

    teacher = relationship("Teacher", back_populates="classes")
    student = relationship("Student", back_populates="classes")
