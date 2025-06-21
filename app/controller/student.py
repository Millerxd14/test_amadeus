from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import student as student_models
from app.schemas import student as student_schemas
from app.utilities.security import get_password_hash

def get_student_by_document_number(db: Session, document_number: str):
    return db.query(student_models.Student).filter(student_models.Student.document_number == document_number).first()

def get_student(db: Session, student_id: int):
    return db.query(student_models.Student).filter(student_models.Student.id == student_id).first()

def get_all_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(student_models.Student).offset(skip).limit(limit).all()

def create_student(db: Session, student: student_schemas.StudentCreate):
    db_student = get_student_by_document_number(db, document_number=student.document_number)
    if db_student:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Document number already registered")
    
    hashed_password = get_password_hash(student.password)
    db_student = student_models.Student(
        first_name=student.first_name,
        last_name=student.last_name,
        age=student.age,
        document_number=student.document_number,
        hashed_password=hashed_password
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db: Session, student_id: int, student: student_schemas.StudentUpdate):
    db_student = get_student(db, student_id)
    if db_student:
        update_data = student.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    db_student = get_student(db, student_id)
    if db_student:
        db.delete(db_student)
        db.commit()
    return db_student
