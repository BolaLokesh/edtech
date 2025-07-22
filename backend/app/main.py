from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from . import models, schemas, crud
from .database import SessionLocal, engine
from .dependencies import get_db, get_current_user, get_current_teacher, get_current_student
from datetime import datetime
import uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoints
@app.post("/api/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/api/login")
def login(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = crud.create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/assignments", response_model=schemas.Assignment)
def create_assignment(
    assignment: schemas.AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_teacher)
):
    return crud.create_assignment(db=db, assignment=assignment, teacher_id=current_user.id)

@app.post("/api/assignments/{assignment_id}/submissions", response_model=schemas.Submission)
def submit_assignment(
    assignment_id: int,
    submission: schemas.SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_student)
):
    return crud.create_submission(db=db, submission=submission, assignment_id=assignment_id, student_id=current_user.id)

@app.get("/api/assignments/{assignment_id}/submissions", response_model=List[schemas.Submission])
def get_submissions(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_teacher)
):
    return crud.get_submissions(db=db, assignment_id=assignment_id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
