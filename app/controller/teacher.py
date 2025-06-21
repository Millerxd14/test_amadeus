from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import teacher as teacher_models
from app.schemas import teacher as teacher_schemas
from app.utilities.security import get_password_hash

def get_teacher_by_document_number(db: Session, document_number: str):
    return db.query(teacher_models.Teacher).filter(teacher_models.Teacher.document_number == document_number).first()

def get_teacher(db: Session, teacher_id: int):
    return db.query(teacher_models.Teacher).filter(teacher_models.Teacher.id == teacher_id).first()

def get_all_teachers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(teacher_models.Teacher).offset(skip).limit(limit).all()

def create_teacher(db: Session, teacher: teacher_schemas.TeacherCreate):
    db_teacher = get_teacher_by_document_number(db, document_number=teacher.document_number)
    if db_teacher:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Document number already registered")
    hashed_password = get_password_hash(teacher.password)
    db_teacher = teacher_models.Teacher(
        first_name=teacher.first_name,
        last_name=teacher.last_name,
        age=teacher.age,
        document_number=teacher.document_number,
        hashed_password=hashed_password
    )
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

def update_teacher(db: Session, teacher_id: int, teacher: teacher_schemas.TeacherUpdate):
    db_teacher = get_teacher(db, teacher_id)
    if db_teacher:
        update_data = teacher.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_teacher, key, value)
        db.commit()
        db.refresh(db_teacher)
    return db_teacher

def delete_teacher(db: Session, teacher_id: int):
    db_teacher = get_teacher(db, teacher_id)
    if db_teacher:
        db.delete(db_teacher)
        db.commit()
    return db_teacher
