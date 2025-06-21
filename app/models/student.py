from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database.connection import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    age = Column(Integer)
    document_number = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)

    classes = relationship("ClassSchedule", back_populates="student")
