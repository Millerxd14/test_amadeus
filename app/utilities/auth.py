
from sqlalchemy.orm import Session
from app.controller import student, teacher
from app.utilities import security


def authenticate_user(db: Session, document_number: str, password: str):
    """
    Authenticates a user (student or teacher) by document number and password.
    """
    # First, try to find a student
    user = student.get_student_by_document_number(db, document_number=document_number)
    if not user:
        # If not a student, try to find a teacher
        user = teacher.get_teacher_by_document_number(db, document_number=document_number)
        kind = "teacher"
    else:
        kind = "student"

    if not user:
        return False
    
    if not security.verify_password(password, user.hashed_password):
        return False
    user.kind = kind 
    return user