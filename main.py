"""
main.py
-------
The actual FastAPI app. Run with:
    uvicorn main:app --reload

Then open http://127.0.0.1:8000/docs for the auto-generated Swagger UI
(you can test everything there too, not just Postman).
"""

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import crud
from database import engine, get_db

# This line creates the `students` table in MySQL if it doesn't exist yet.
# (Runs once at startup — reads models.py and issues CREATE TABLE.)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Placement API")


@app.get("/")
def root():
    return {"message": "Student API is running. Visit /docs to test it."}


# ---------- 1. ADD STUDENT ----------
@app.post("/students", response_model=schemas.StudentOut, status_code=201)
def add_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)


# ---------- 2. GET STUDENT ----------
@app.get("/students/{student_id}", response_model=schemas.StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


# Bonus: get ALL students (useful for testing/demoing)
@app.get("/students", response_model=List[schemas.StudentOut])
def get_all_students(db: Session = Depends(get_db)):
    return crud.get_all_students(db)


# ---------- 3. UPDATE STUDENT ----------
@app.put("/students/{student_id}", response_model=schemas.StudentOut)
def update_student(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    db_student = crud.update_student(db, student_id, student)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


# ---------- 4. DELETE STUDENT ----------
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.delete_student(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": f"Student {student_id} deleted successfully"}


# ---------- 5. DELETE ALL STUDENTS (bulk) ----------
# WARNING: this wipes the entire table. Handy for resetting test data,
# but in a real production API you'd usually restrict or remove this
# entirely — there's no confirmation step, one call empties everything.
@app.delete("/students")
def delete_all_students(db: Session = Depends(get_db)):
    count = crud.delete_all_students(db)
    return {"message": f"Deleted {count} student(s) successfully"}

