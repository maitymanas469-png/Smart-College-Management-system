"""Smart College Management System : BACKEND (Flask + SQLite)
Run:  pip install flask   then   python app.py   -> open http://127.0.0.1:5000
"""
import os, sqlite3
from flask import Flask, request, jsonify

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "..", "database", "college.db")
SCHEMA = os.path.join(BASE, "..", "database", "schema.sql")
app = Flask(__name__, static_folder=os.path.join(BASE, "..", "frontend"), static_url_path="")

def run(sql, args=(), write=False):
    """One helper for every SQL query."""
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    try:
        cur = con.execute(sql, args)
        if write:
            con.commit()
            return cur.lastrowid
        return [dict(r) for r in cur.fetchall()]
    finally:
        con.close()

def init_db():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    if not os.path.exists(DB):
        con = sqlite3.connect(DB)
        con.executescript(open(SCHEMA).read())
        con.commit()
        con.close()

@app.errorhandler(sqlite3.Error)
def db_error(e):
    return jsonify(error=str(e)), 400

@app.route("/")
def home():
    return app.send_static_file("index.html")

# ---------- Raw Database Explorer Endpoint ----------
@app.get("/api/raw-db")
def raw_db():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [row["name"] for row in cursor.fetchall()]
    
    data = {}
    for t in tables:
        cur = con.execute(f"SELECT * FROM {t}")
        data[t] = [dict(r) for r in cur.fetchall()]
    con.close()
    return jsonify(data)

# ---------- Departments & Courses ----------
@app.get("/api/departments")
def departments():
    return jsonify(run("SELECT * FROM department"))

@app.get("/api/courses")
def courses():
    return jsonify(run("""SELECT c.course_id, c.course_name, c.credits, d.dept_name,
        (SELECT COUNT(*) FROM enrollment e WHERE e.course_id = c.course_id) AS enrolled
        FROM course c JOIN department d ON d.dept_id = c.dept_id"""))

@app.post("/api/courses")
def add_course():
    d = request.json
    run("INSERT INTO course(course_name,credits,dept_id) VALUES (?,?,?)",
        (d["course_name"], d.get("credits", 3), d["dept_id"]), write=True)
    return jsonify(ok=True)

# ---------- Students ----------
@app.get("/api/students")
def students():
    return jsonify(run("""SELECT s.*, d.dept_name FROM student s
        JOIN department d ON d.dept_id = s.dept_id ORDER BY s.roll_no"""))

@app.post("/api/students")
def add_student():
    d = request.json
    run("INSERT INTO student(roll_no,name,email,year,total_fee,dept_id) VALUES (?,?,?,?,?,?)",
        (d["roll_no"], d["name"], d.get("email"), d["year"], d.get("total_fee", 0), d["dept_id"]), write=True)
    return jsonify(ok=True)

@app.delete("/api/students/<int:sid>")
def del_student(sid):
    run("DELETE FROM student WHERE student_id = ?", (sid,), write=True)
    return jsonify(ok=True)

@app.post("/api/enroll")
def enroll():
    d = request.json
    run("INSERT INTO enrollment VALUES (?,?)", (d["student_id"], d["course_id"]), write=True)
    return jsonify(ok=True)

# ---------- Attendance ----------
@app.get("/api/attendance")
def attendance():
    """Attendance % per student per course."""
    return jsonify(run("""SELECT s.name, c.course_name,
        COUNT(a.att_id) AS total,
        SUM(a.status = 'Present') AS present,
        ROUND(100.0 * SUM(a.status = 'Present') / COUNT(a.att_id), 1) AS percent
        FROM attendance a JOIN student s ON s.student_id = a.student_id
        JOIN course c ON c.course_id = a.course_id
        GROUP BY a.student_id, a.course_id"""))

@app.post("/api/attendance")
def mark_attendance():
    d = request.json
    run("INSERT OR REPLACE INTO attendance(student_id,course_id,att_date,status) VALUES (?,?,?,?)",
        (d["student_id"], d["course_id"], d["att_date"], d["status"]), write=True)
    return jsonify(ok=True)

# ---------- Fees ----------
@app.get("/api/fees")
def fees():
    return jsonify(run("""SELECT s.student_id, s.name, s.total_fee,
        IFNULL(SUM(f.amount),0) AS paid,
        s.total_fee - IFNULL(SUM(f.amount),0) AS pending
        FROM student s LEFT JOIN fee_payment f ON f.student_id = s.student_id
        GROUP BY s.student_id"""))

@app.post("/api/fees")
def pay_fee():
    d = request.json
    run("INSERT INTO fee_payment(student_id,amount) VALUES (?,?)",
        (d["student_id"], d["amount"]), write=True)
    return jsonify(ok=True)

# ---------- Dashboard ----------
@app.get("/api/dashboard")
def dashboard():
    one = lambda q: run(q)[0]["n"]
    return jsonify(students=one("SELECT COUNT(*) n FROM student"),
                   courses=one("SELECT COUNT(*) n FROM course"),
                   collected=one("SELECT IFNULL(SUM(amount),0) n FROM fee_payment"),
                   pending=one("SELECT IFNULL(SUM(total_fee),0) - (SELECT IFNULL(SUM(amount),0) FROM fee_payment) n FROM student"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)