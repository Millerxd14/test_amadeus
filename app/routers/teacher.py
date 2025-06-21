from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List


from app.controller import teacher as teracher_crud
from app.schemas import teacher as teacher_schemas
from ..database.connection import get_db

router = APIRouter(
    tags=["Teachers"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=teacher_schemas.TeacherInDB, status_code=status.HTTP_201_CREATED)
def create_teacher(teacher: teacher_schemas.TeacherCreate, db: Session = Depends(get_db)):
    return teracher_crud.create_teacher(db=db, teacher=teacher)

@router.get("/", response_model=List[teacher_schemas.TeacherInDB])
def read_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    teachers = teracher_crud.get_all_teachers(db, skip=skip, limit=limit)
    return teachers

@router.get("/{teacher_id}", response_model=teacher_schemas.TeacherInDB)
def read_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = teracher_crud.get_teacher(db, teacher_id=teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher

@router.put("/{teacher_id}", response_model=teacher_schemas.TeacherInDB)
def update_teacher(teacher_id: int, teacher: teacher_schemas.TeacherUpdate, db: Session = Depends(get_db)):
    db_teacher = teracher_crud.update_teacher(db, teacher_id=teacher_id, teacher=teacher)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher

@router.delete("/{teacher_id}", response_model=teacher_schemas.TeacherInDB)
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = teracher_crud.delete_teacher(db, teacher_id=teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher
