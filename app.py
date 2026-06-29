from flask import Flask, render_template, request, redirect, session, send_from_directory, flash
import sqlite3
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "student_notes_secret_key"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id, username, password FROM users WHERE username=?",
            (username,)
        )

        user = cursor.fetchone()

        connection.close()

        if user and check_password_hash(user[2], password):

            session["user_id"] = user[0]
            session["username"] = user[1]

            flash("Login Successful! Welcome back.", "success")

            return redirect("/dashboard")

        else:

            flash("Invalid Username or Password!", "danger")

            return redirect("/login")

    return render_template("login.html")

       

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Encrypt the password
        hashed_password = generate_password_hash(password)

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        # Check if username or email already exists
        cursor.execute(
            "SELECT * FROM users WHERE username=? OR email=?",
            (username, email)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            connection.close()
            return "Username or Email already exists!"

        cursor.execute(
            "INSERT INTO users(username, email, password) VALUES(?,?,?)",
            (username, email, hashed_password)
        )

        connection.commit()
        connection.close()

        return redirect("/login")

    return render_template("register.html")
       


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM notes
        WHERE user_id = ?
        """,
        (session["user_id"],)
    )

    total_notes = cursor.fetchone()[0]

    connection.close()

    return render_template(
        "dashboard.html",
        username=session["username"],
        total_notes=total_notes
    )

# ---------------- UPLOAD ----------------
@app.route("/upload", methods=["GET", "POST"])
def upload():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        title = request.form["title"]
        subject = request.form["subject"]

        file = request.files["file"]

        if file:

            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO notes(title, subject, filename, user_id)
                VALUES (?, ?, ?, ?)
                """,
                (
                    title,
                    subject,
                    filename,
                    session["user_id"]
                )
            )

            connection.commit()
            connection.close()

            return redirect("/notes")

    return render_template("upload.html")

# ---------------- VIEW NOTES ----------------
@app.route("/notes")
def notes():

    if "user_id" not in session:
        return redirect("/login")

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, title, subject, filename
        FROM notes
        WHERE user_id = ?
        """,
        (session["user_id"],)
    )

    notes = cursor.fetchall()

    connection.close()

    return render_template("notes.html", notes=notes)


# ---------------- SEARCH ----------------
@app.route("/search")
def search():

    if "user_id" not in session:
        return redirect("/login")

    keyword = request.args.get("search")

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, title, subject, filename
        FROM notes
        WHERE user_id = ? AND title LIKE ?
        """,
        (session["user_id"], "%" + keyword + "%")
    )

    notes = cursor.fetchall()

    connection.close()

    return render_template("notes.html", notes=notes)


# ---------------- DELETE ----------------
@app.route("/delete/<int:id>")
def delete(id):

    if "user_id" not in session:
        return redirect("/login")

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM notes
        WHERE id = ? AND user_id = ?
        """,
        (id, session["user_id"])
    )

    connection.commit()
    connection.close()

    return redirect("/notes")


# ---------------- DOWNLOAD ----------------
@app.route("/download/<filename>")
def download(filename):

    if "user_id" not in session:
        return redirect("/login")

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM notes
        WHERE filename = ? AND user_id = ?
        """,
        (filename, session["user_id"])
    )

    note = cursor.fetchone()

    connection.close()

    if note:
        return send_from_directory(
            app.config["UPLOAD_FOLDER"],
            filename,
            as_attachment=True
        )

    return "Access Denied!"

# ---------------- USERS ----------------
@app.route("/users")
def users():

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users")

    users = cursor.fetchall()

    connection.close()

    return str(users)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.pop("username", None)

    return redirect("/")

@app.route("/allnotes")
def allnotes():

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM notes")

    notes = cursor.fetchall()

    connection.close()

    return str(notes)

@app.route("/session")
def check_session():
    return str(session)

if __name__ == "__main__":
    app.run(debug=True)