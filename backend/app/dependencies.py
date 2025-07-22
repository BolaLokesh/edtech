from fastapi import Depends
from sqlalchemy.orm import Session
from . import schemas, auth
from .database import get_db

def get_current_user(token: str = Depends(auth.oauth2_scheme), db: Session = Depends(get_db)):
    return auth.get_current_user(token, db)

def get_current_student(current_user: schemas.User = Depends(get_current_user)):
    return auth.get_current_student(current_user)

def get_current_teacher(current_user: schemas.User = Depends(get_current_user)):
    return auth.get_current_teacher(current_user)
