import os
import sqlite3
from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-development-key")

DB_NAME = "users.db"

# Create or update DB schema
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT
        )
    ''')

    # Handle an older database created by the vulnerable version.
    columns = [row[1] for row in cursor.execute("PRAGMA table_info(users)").fetchall()]

    if "password_hash" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")

    if "password" in columns:
        old_users = cursor.execute(
            "SELECT id, password FROM users WHERE password_hash IS NULL"
        ).fetchall()

        for user_id, old_password in old_users:
            if old_password is not None:
                cursor.execute(
                    "UPDATE users SET password_hash = ? WHERE id = ?",
                    (generate_password_hash(old_password), user_id)
                )

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

        conn = sqlite3.connect(DB_NAME)
        try:
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
        except sqlite3.IntegrityError:
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

        conn = sqlite3.connect(DB_NAME)
        result = conn.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        conn.close()

        if result and result[2] and check_password_hash(result[2], password):
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
