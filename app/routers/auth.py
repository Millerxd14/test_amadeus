from datetime import timedelta
import json

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..utilities import security

from app.schemas import token as schemas_token
from ..database.connection import get_db
from ..utilities.auth import authenticate_user

router = APIRouter(
    tags=["Authentication"],
)

@router.post("/token", response_model=schemas_token.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, document_number=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect document number or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30) # Or load from config
    access_token = security.create_access_token(
        data={"sub": json.dumps({ "id":user.id, "kind": user.kind })},
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "kind": user.kind
        }
