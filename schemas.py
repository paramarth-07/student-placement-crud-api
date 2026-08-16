"""
schemas.py
----------
These are Pydantic models — NOT database models.
They define what shape of JSON the API expects to RECEIVE (request body)
and what shape it will SEND BACK (response body).

Keeping these separate from models.py (the DB layer) is standard practice:
DB structure and API contract are allowed to evolve independently.
"""

from pydantic import BaseModel
from typing import Optional


class StudentBase(BaseModel):
    name: str
    age: int
    course: str
    placement_status: Optional[str] = "Not Placed"
    company: Optional[str] = None
    package_lpa: Optional[float] = None


class StudentCreate(StudentBase):
    """Used for POST /students (Add Student) — no id yet, DB generates it."""
    pass


class StudentUpdate(BaseModel):
    """
    Used for PUT /students/{id} (Update Student).
    All fields optional, so the client can send only what they want to change.
    """
    name: Optional[str] = None
    age: Optional[int] = None
    course: Optional[str] = None
    placement_status: Optional[str] = None
    company: Optional[str] = None
    package_lpa: Optional[float] = None


class StudentOut(StudentBase):
    """Used when SENDING a student back to the client — includes id."""
    id: int

    class Config:
        from_attributes = True  # allows Pydantic to read data from ORM objects directly
