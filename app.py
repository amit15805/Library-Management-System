from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "library.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------------------------
# MODELS
# -------------------------

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150))
    copies = db.Column(db.Integer, default=1)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    roll_no = db.Column(db.String(50), unique=True, nullable=False)

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    issue_date = db.Column(db.String(30))
    return_date = db.Column(db.String(30))


with app.app_context():
    db.create_all()

# -------------------------
# ROUTES
# -------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/books")
def books_page():
    return render_template("books.html")

@app.route("/students")
def students_page():
    return render_template("students.html")

@app.route("/issue")
def issue_page():
    return render_template("issue.html")

# -------------------------
# API ENDPOINTS
# -------------------------

@app.route("/api/books", methods=["GET"])
def get_books():
    books = Book.query.all()
    return jsonify([{"id": b.id, "title": b.title, "author": b.author, "copies": b.copies} for b in books])

@app.route("/api/books", methods=["POST"])
def add_book():
    data = request.json
    book = Book(title=data["title"], author=data["author"], copies=data["copies"])
    db.session.add(book)
    db.session.commit()
    return jsonify({"message": "Book added"})

@app.route("/api/books/<int:id>", methods=["DELETE"])
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"})

@app.route("/api/students", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([{"id": s.id, "name": s.name, "roll_no": s.roll_no} for s in students])

@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.json
    student = Student(name=data["name"], roll_no=data["roll_no"])
    db.session.add(student)
    db.session.commit()
    return jsonify({"message": "Student added"})

@app.route("/api/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted"})

@app.route("/api/issue", methods=["POST"])
def issue_book():
    data = request.json
    issue = Issue(
        student_id=data["student_id"],
        book_id=data["book_id"],
        issue_date=datetime.now().strftime("%Y-%m-%d"),
        return_date=""
    )

    book = Book.query.get(data["book_id"])
    if book.copies <= 0:
        return jsonify({"error": "No copies available"}), 400

    book.copies -= 1
    db.session.add(issue)
    db.session.commit()
    return jsonify({"message": "Book issued"})

@app.route("/api/return/<int:id>", methods=["POST"])
def return_book(id):
    issue = Issue.query.get(id)
    issue.return_date = datetime.now().strftime("%Y-%m-%d")

    book = Book.query.get(issue.book_id)
    book.copies += 1
    db.session.commit()
    return jsonify({"message": "Book returned"})

@app.route("/api/issued", methods=["GET"])
def issued_books():
    issues = Issue.query.all()
    data = []
    for i in issues:
        student = Student.query.get(i.student_id)
        book = Book.query.get(i.book_id)
        data.append({
            "id": i.id,
            "student": student.name,
            "roll_no": student.roll_no,
            "book": book.title,
            "issue_date": i.issue_date,
            "return_date": i.return_date
        })
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)