"""
models.py
---------
This defines the actual MySQL TABLE structure, but written as a Python class.
SQLAlchemy converts this class into a `CREATE TABLE` statement for you.

Table: students
Columns: id, name, age, course, placement_status, company, package_lpa
"""

from sqlalchemy import Column, Integer, String, Float
from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    course = Column(String(100), nullable=False)

    # Placement record fields (as per your task: "Store placement records")
    placement_status = Column(String(20), default="Not Placed")  # Placed / Not Placed
    company = Column(String(100), nullable=True)
    package_lpa = Column(Float, nullable=True)  # package in LPA (Lakhs Per Annum)
