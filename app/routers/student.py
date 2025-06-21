from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.controller import student as student_crud
from app.schemas import student as schemas
from ..database.connection import get_db

router = APIRouter(
    tags=["Students"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.StudentInDB, status_code=status.HTTP_201_CREATED)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return student_crud.create_student(db=db, student=student)

@router.get("/", response_model=List[schemas.StudentInDB])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = student_crud.get_all_students(db, skip=skip, limit=limit)
    return students

@router.get("/{student_id}", response_model=schemas.StudentInDB)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = student_crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.put("/{student_id}", response_model=schemas.StudentInDB)
def update_student(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    db_student = student_crud.update_student(db, student_id=student_id, student=student)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.delete("/{student_id}", response_model=schemas.StudentInDB)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = student_crud.delete_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student
