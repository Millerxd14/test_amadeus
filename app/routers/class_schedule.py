from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from ..schemas.class_schedule import ClassScheduleBase, ClassScheduleCreate, ClassScheduleUpdate, ClassScheduleInDB
from ..database.connection import get_db
from ..controller import class_schedule as crud_class_schedule

# Define el router para las clases
router = APIRouter(
    tags=["Class Schedules"],
    responses={404: {"description": "Not found"}},
)

# --- Endpoints del CRUD ---

@router.post("/", response_model=ClassScheduleInDB, status_code=status.HTTP_201_CREATED)
async def create_class(class_data: ClassScheduleCreate, db: Session = Depends(get_db)):
    
    return crud_class_schedule.create_class_schedule(db=db, class_schedule=class_data)

@router.get("/", response_model=List[ClassScheduleInDB])
async def get_all_classes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    
    classes = crud_class_schedule.get_all_class_schedules(db, skip=skip, limit=limit)
    return classes
    

@router.get("/{class_id}", response_model=ClassScheduleInDB)
async def get_class_by_id(class_id: int, db: Session = Depends(get_db)):
    db_class = crud_class_schedule.get_class_schedule(db, class_schedule_id=class_id)
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return db_class

@router.put("/{class_id}", response_model=ClassScheduleInDB)
async def update_class(class_id: int, class_data: ClassScheduleUpdate, db: Session = Depends(get_db)):
    db_class = crud_class_schedule.update_class_schedule(db, class_schedule_id=class_id, class_schedule=class_data)
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return db_class

@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_class(class_id: int, db: Session = Depends(get_db)):
    db_class = crud_class_schedule.delete_class_schedule(db, class_schedule_id=class_id)
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return