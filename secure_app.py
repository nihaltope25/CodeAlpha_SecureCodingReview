import os
import sqlite3
from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-development-key")

# Create DB
def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

app.config["MAX_LOGIN_ATTEMPTS"] = 5

@app.route("/")
def home():
    return render_template("index.html")

# SECURE REGISTER: parameterized query + password hashing
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            return "Username and password are required", 400

        password_hash = generate_password_hash(password)

        conn = sqlite3.connect("users.db")
        try:
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists", 409
        finally:
            conn.close()

        return redirect("/login")

    return render_template("register.html")

# SECURE LOGIN: parameterized query + hashed password verification
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Basic brute-force protection for the current session
        if session.get("login_attempts", 0) >= app.config["MAX_LOGIN_ATTEMPTS"]:
            return "Account temporarily locked. Try again later.", 429

        conn = sqlite3.connect("users.db")
        result = conn.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        conn.close()

        if result and check_password_hash(result[2], password):
            session.clear()
            session["user"] = result[1]
            return redirect("/dashboard")

        session["login_attempts"] = session.get("login_attempts", 0) + 1
        return "Invalid Credentials", 401

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html", user=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=False)