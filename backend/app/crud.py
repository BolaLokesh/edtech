from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas, auth

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role,
        created_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, user: schemas.UserLogin):
    db_user = get_user_by_email(db, email=user.email)
    if not db_user:
        return False
    if not auth.verify_password(user.password, db_user.hashed_password):
        return False
    access_token = auth.create_access_token(
        data={"sub": db_user.email, "role": db_user.role},
        expires_delta=timedelta(minutes=auth.settings.access_token_expire_minutes)
    )
    return {"access_token": access_token, "token_type": "bearer"}

def create_assignment(db: Session, assignment: schemas.AssignmentCreate, teacher_id: int):
    db_assignment = models.Assignment(
        **assignment.dict(),
        teacher_id=teacher_id,
        created_at=datetime.utcnow()
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

def create_submission(db: Session, submission: schemas.SubmissionCreate, assignment_id: int, student_id: int):
    db_submission = models.Submission(
        **submission.dict(),
        assignment_id=assignment_id,
        student_id=student_id,
        submitted_at=datetime.utcnow()
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

def get_submissions(db: Session, assignment_id: int):
    return db.query(models.Submission).filter(models.Submission.assignment_id == assignment_id).all()
