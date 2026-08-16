# Student Placement API — FastAPI + MySQL + Postman

## Project layout
```
student_api/
├── database.py   # MySQL connection (SQLAlchemy engine + session)
├── models.py     # Student table definition (ORM)
├── schemas.py    # Request/response validation (Pydantic)
├── crud.py       # Create/Read/Update/Delete logic
├── main.py       # FastAPI routes
└── requirements.txt
```

---

## Part 1: Install & set up MySQL

### 1. Install MySQL
- **Windows:** download MySQL Installer from mysql.com, install "MySQL Server" + "MySQL Workbench".
- **Mac:** `brew install mysql && brew services start mysql`
- **Linux:** `sudo apt install mysql-server && sudo systemctl start mysql`

### 2. Log in and create your database
Open a terminal:
```bash
mysql -u root -p
```
Then inside the MySQL prompt:
```sql
CREATE DATABASE student_db;
SHOW DATABASES;   -- confirm it's there
EXIT;
```
That's it — you do **not** need to manually create the `students` table.
SQLAlchemy does that for you automatically the first time you run the app
(look at the `models.Base.metadata.create_all(bind=engine)` line in `main.py`).

### 3. Update your credentials
Open `database.py` and edit:
```python
MYSQL_USER = "root"
MYSQL_PASSWORD = "your_password"   # <-- your actual MySQL root password
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DB = "student_db"
```

### 4. Useful MySQL commands while you're learning
```sql
USE student_db;
SHOW TABLES;
DESCRIBE students;
SELECT * FROM students;
```
Every time you hit an API endpoint, come back to this prompt and run
`SELECT * FROM students;` to *see* the change happen. That side-by-side
habit is the fastest way to actually learn what the ORM is doing.

---

## Part 2: Run the API

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
You should see log lines including `CREATE TABLE students (...)` (because
`echo=True` is set in `database.py` — it prints every SQL statement,
which is great for learning; turn it off later).

Open **http://127.0.0.1:8000/docs** — this is FastAPI's built-in Swagger
UI. You can test every endpoint here with zero setup, before even
touching Postman.

---

## Part 3: Learn Postman

### 1. Install & open Postman
Download from postman.com. Create a free account (or skip/guest mode).

### 2. Create a Collection
- Click **New → Collection**, name it `Student API`.
- Inside it, create one request per endpoint (see table below). Saving
  requests in a collection means you don't retype the URL every time.

### 3. The 4 requests to create

| # | Name | Method | URL | Body (raw JSON) |
|---|------|--------|-----|------------------|
| 1 | Add Student | POST | `http://127.0.0.1:8000/students` | see below |
| 2 | Get Student | GET | `http://127.0.0.1:8000/students/1` | none |
| 3 | Update Student | PUT | `http://127.0.0.1:8000/students/1` | see below |
| 4 | Delete Student | DELETE | `http://127.0.0.1:8000/students/1` | none |

**Add Student — Body tab → raw → JSON:**
```json
{
  "name": "Riya Sharma",
  "age": 21,
  "course": "Computer Science",
  "placement_status": "Placed",
  "company": "TCS",
  "package_lpa": 6.5
}
```

**Update Student — Body tab → raw → JSON** (only send fields you want to change):
```json
{
  "placement_status": "Placed",
  "company": "Infosys",
  "package_lpa": 7.2
}
```

### 4. How to set the body correctly in Postman
1. Select the request.
2. Click the **Body** tab (below the URL bar).
3. Select **raw**.
4. On the dropdown to the right of "raw", pick **JSON**.
5. Paste the JSON.
6. Hit **Send**.

### 5. Suggested test flow (do this in order)
1. Run **Add Student** two or three times with different names → note the
   `id` values returned in the response.
2. Run **GET `/students`** (no id — returns the full list) to see all of them.
3. Run **Get Student** with one of those ids.
4. Run **Update Student** on that id, changing `placement_status` and
   `company` (simulate a student getting placed).
5. Run **Get Student** again on the same id to confirm the update stuck.
6. Run **Delete Student** on it.
7. Run **Get Student** again on that same id → you should now get a
   `404 Student not found`. That confirms delete worked.

### 6. Reading responses
- **Status code** (top right of the response panel): `201` = created,
  `200` = OK, `404` = not found, `422` = your JSON body is malformed or
  missing a required field — check it against the schema in `schemas.py`.
- **Body** tab shows the JSON FastAPI sent back.

---

## Notes tying this back to your task list
- **Connect Python with MySQL** → `database.py` (the `create_engine(...)` line).
- **Perform CRUD operations** → `crud.py` functions, exposed as routes in `main.py`.
- **Store placement records** → the `placement_status`, `company`, and
  `package_lpa` columns on the `Student` model already cover this. If
  your internship wants a *separate* placements table linked to students
  (one student → many placement records, e.g. multiple offers), say so
  and I'll extend this with a proper foreign-key relationship — that's
  a very reasonable next step once basic CRUD is working.
