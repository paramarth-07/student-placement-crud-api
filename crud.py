"""
crud.py
-------
CRUD = Create, Read, Update, Delete.

This file is the "database logic" layer. main.py (the API routes) calls
these functions instead of writing SQLAlchemy queries directly in the
route — this separation makes code easier to test and reuse.

Each function takes a `db: Session` (the live MySQL connection for this
request) as its first argument.
"""

from sqlalchemy.orm import Session
import models
import schemas


def create_student(db: Session, student: schemas.StudentCreate):
    # Convert Pydantic model -> dict -> unpack into SQLAlchemy model
    db_student = models.Student(**student.model_dump())
    db.add(db_student)      # stage the INSERT
    db.commit()             # actually run: INSERT INTO students (...) VALUES (...)
    db.refresh(db_student)  # reload from DB so db_student.id is populated
    return db_student


def get_student(db: Session, student_id: int):
    # Equivalent raw SQL: SELECT * FROM students WHERE id = %s LIMIT 1
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def get_all_students(db: Session, skip: int = 0, limit: int = 100):
    # Equivalent raw SQL: SELECT * FROM students LIMIT %s OFFSET %s
    return db.query(models.Student).offset(skip).limit(limit).all()


def update_student(db: Session, student_id: int, student: schemas.StudentUpdate):
    db_student = get_student(db, student_id)
    if db_student is None:
        return None

    # Only update fields the client actually sent (exclude_unset=True)
    update_data = student.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int):
    db_student = get_student(db, student_id)
    if db_student is None:
        return None
    db.delete(db_student)   # DELETE FROM students WHERE id = %s
    db.commit()
    return db_student


def delete_all_students(db: Session):
    # Equivalent raw SQL: DELETE FROM students;
    # Returns how many rows were deleted so the API can report it back.
    count = db.query(models.Student).delete()
    db.commit()
    return count

