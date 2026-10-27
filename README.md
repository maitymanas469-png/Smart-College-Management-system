# 🎓 Smart College Management System

A lightweight, browser-based college management application built with **Python (Flask)**, **SQLite**, and **HTML/CSS/JavaScript**. It brings student records, courses, attendance, fee payments, and summary statistics into one simple dashboard.

## ✨ Features

- **Dashboard:** View total students, courses, fees collected, and pending fees.
- **Student management:** Add, list, and delete student records, with department and year information.
- **Course management:** Add courses, view their credits and departments, and enroll students.
- **Attendance:** Mark students as Present or Absent by course and date; view attendance percentages for recorded entries.
- **Fee management:** Record student payments and see paid and pending balances.
- **Database explorer:** Inspect the contents of all application tables in the **All Data** tab.

## 🛠️ Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | HTML5, CSS3, vanilla JavaScript |
| Backend | Python, Flask |
| Database | SQLite |
| API | JSON-based REST-style HTTP endpoints |

## 📁 Project Structure

Organize the provided files like this (rename `app(3).py` to `app.py`):

```text
smart-college-management-system/
├── backend/
│   └── app.py
├── database/
│   ├── schema.sql
│   └── college.db          # Created automatically on first run
├── frontend/
│   └── index.html
├── .gitignore              # Recommended
└── README.md
```

> **Important:** The backend uses paths relative to its own folder. Keep `backend`, `database`, and `frontend` as sibling folders, as shown above.

## 🚀 Getting Started

### Prerequisites

- Python 3 installed
- `pip` (included with most Python installations)
- A modern web browser

### 1. Download the project

Clone your GitHub repository or download its ZIP file and open the project folder in VS Code.

### 2. Create a virtual environment (recommended)

From the project root, in the VS Code terminal:

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install flask
```

**macOS / Linux:**

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install flask
```

Using the virtual environment's Python directly avoids needing to activate it in PowerShell.

### 3. Run the Flask server

**Windows:**

```powershell
.\.venv\Scripts\python.exe backend\app.py
```

**macOS / Linux:**

```bash
./.venv/bin/python backend/app.py
```

### 4. Open the application

Visit **http://127.0.0.1:5000** in your browser.

On first startup, Flask initializes `database/college.db` using `database/schema.sql` and loads the included sample records. **No separate database server or manual SQL import is required.**

## 🧭 How to Use

1. Open **Dashboard** to see college-wide statistics.
2. Open **Students** to add or remove student records.
3. Open **Courses** to create courses and enroll students.
4. Open **Attendance** to mark attendance for a selected student, course, and date.
5. Open **Fees** to record payments and check outstanding balances.
6. Open **All Data** to inspect the underlying database tables.

## 🗄️ Database Design

The SQLite database contains six related tables:

| Table | Purpose |
| --- | --- |
| `department` | Stores department names |
| `student` | Stores roll number, name, email, year, total fee, and department |
| `course` | Stores course name, credits, and department |
| `enrollment` | Connects students and courses (many-to-many) |
| `attendance` | Stores attendance status for a student, course, and date |
| `fee_payment` | Stores student payment amounts and dates |

**Relationships:**

- One department can have many students and courses.
- Students and courses have a many-to-many relationship through `enrollment`.
- Attendance entries reference a student and a course.
- Fee payments reference a student.

The schema includes foreign keys, unique constraints, and checks for valid years, attendance statuses, and positive payment amounts.

### Example: Add a Student

Send a `POST` request to `/api/students` with a JSON body:

```json
{
  "roll_no": "CS103",
  "name": "Example Student",
  "email": "student@example.com",
  "year": 2,
  "total_fee": 60000,
  "dept_id": 1
}
```

A successful request returns:

```json
{"ok": true}
```
## 🔐 Notes and Limitations

This is an educational prototype, **not a production-ready college administration system**.

- There is currently no login system or role-based access control.
- The **All Data** endpoint exposes database records; it should not be publicly accessible without authentication and authorization.
- Flask runs with `debug=True` in the supplied backend. Disable debug mode for any deployment.
- The frontend uses dynamically generated HTML and should be hardened against unsafe content before accepting untrusted input.
- Attendance percentages are calculated from recorded attendance entries only.
- Deleting a student also deletes their related enrollment, attendance, and payment records because of cascading foreign keys.

## 🔮 Possible Future Improvements

- Administrator, faculty, and student login
- Role-based permissions
- Student search and filtering
- Attendance reports and exports
- Payment history and receipts
- Improved form validation and error messages
- Responsive UI enhancements
- Automated testing and production deployment configuration

## 👨‍💻 Project Author

**Manas Maity**  
B.Tech — Computer Science and Engineering  
Brainware University

## 📌 Project Status

**Educational prototype** — Core CRUD and reporting features are implemented in the supplied source files. Additional security, testing, and deployment work would be needed before real-world use.
