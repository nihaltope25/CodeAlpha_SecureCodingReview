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
            username TEXT,
            password TEXT,
            password_hash TEXT
        )
    ''')

    columns = [row[1] for row in cursor.execute("PRAGMA table_info(users)").fetchall()]

    # Add the secure password_hash column to an older database if necessary.
    if "password_hash" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
        columns.append("password_hash")

    # Migrate passwords from the old vulnerable database to hashes.
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
            # Check for an existing username before inserting.
            existing = conn.execute(
                "SELECT id FROM users WHERE username = ?",
                (username,)
            ).fetchone()

            if existing:
                return "Username already exists", 409

            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
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

        # Basic brute-force protection for the current session.
        if session.get("login_attempts", 0) >= app.config["MAX_LOGIN_ATTEMPTS"]:
            return "Account temporarily locked. Try again later.", 429

        conn = sqlite3.connect(DB_NAME)
        result = conn.execute(
            "SELECT id, username, password_hash, password FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if result:
            user_id, stored_username, password_hash, legacy_password = result

            # Normal secure login path.
            valid_password = (
                bool(password_hash) and check_password_hash(password_hash, password)
            )

            # Compatibility path for an old database record. If an old plain-text
            # password still exists, verify it once and immediately replace it with
            # a hash. This lets existing local databases continue to work.
            if not valid_password and legacy_password is not None:
                if password == legacy_password:
                    password_hash = generate_password_hash(password)
                    conn.execute(
                        "UPDATE users SET password_hash = ?, password = NULL WHERE id = ?",
                        (password_hash, user_id)
                    )
                    conn.commit()
                    valid_password = True

            conn.close()

            if valid_password:
                session.clear()
                session["user"] = stored_username
                return redirect("/dashboard")
        else:
            conn.close()

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
