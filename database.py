"""
database.py
------------
This is where Python connects to MySQL.

We use SQLAlchemy as an ORM (Object Relational Mapper) so we don't have
to write raw SQL for every operation — though you CAN still write raw
SQL if you want (see crud.py comments for both styles).

Connection string format for MySQL + PyMySQL driver:
    mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

# Load variables from a local .env file (never committed to GitHub)
load_dotenv()

# ---- These now come from environment variables (see .env / .env.example) ----
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "your_password")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DB", "student_db")

# quote_plus escapes special characters (@, :, /, # etc.) so a password
# like "Pass@123" doesn't break the connection string below — without
# this, an "@" in your password gets misread as the separator between
# password and host, causing a confusing "getaddrinfo failed" error.
MYSQL_PASSWORD_ESCAPED = quote_plus(MYSQL_PASSWORD)

DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD_ESCAPED}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

# The engine manages the actual connection pool to MySQL
engine = create_engine(DATABASE_URL, echo=True)  # echo=True prints SQL to console (good for learning)

# Each SessionLocal() instance is a database session/conversation
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that our ORM models will inherit from
Base = declarative_base()


def get_db():
    """
    Dependency function used by FastAPI routes.
    Opens a DB session, yields it to the route, then closes it
    afterwards (even if an error occurs) — this pattern is called
    a 'context-managed dependency'.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()