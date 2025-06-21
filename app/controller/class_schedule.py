from sqlalchemy.orm import Session, joinedload
from app.models import class_schedule as class_models
from app.schemas import class_schedule as class_schemas

def get_class_schedule(db: Session, class_schedule_id: int):
    return db.query(class_models.ClassSchedule).options(
        joinedload(class_models.ClassSchedule.teacher, innerjoin=True),
        joinedload(class_models.ClassSchedule.student, innerjoin=True)
    ).filter(class_models.ClassSchedule.id == class_schedule_id).first()

def get_all_class_schedules(db: Session, skip: int = 0, limit: int = 100):
    return db.query(class_models.ClassSchedule).options(
        joinedload(class_models.ClassSchedule.teacher, innerjoin=True),
        joinedload(class_models.ClassSchedule.student, innerjoin=True)
    ).offset(skip).limit(limit).all()

def create_class_schedule(db: Session, class_schedule: class_schemas.ClassScheduleCreate):
    db_class_schedule = class_models.ClassSchedule(**class_schedule.model_dump())
    db.add(db_class_schedule)
    db.commit()
    db.refresh(db_class_schedule)
    return db_class_schedule

def update_class_schedule(db: Session, class_schedule_id: int, class_schedule: class_schemas.ClassScheduleUpdate):
    db_class_schedule = get_class_schedule(db, class_schedule_id)
    if db_class_schedule:
        update_data = class_schedule.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_class_schedule, key, value)
        db.commit()
        db.refresh(db_class_schedule)
    return db_class_schedule

def delete_class_schedule(db: Session, class_schedule_id: int):
    db_class_schedule = get_class_schedule(db, class_schedule_id)
    if db_class_schedule:
        db.delete(db_class_schedule)
        db.commit()
    return db_class_schedule
