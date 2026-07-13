from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# Create DB
def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

# ❌ VULNERABLE REGISTER (SQL Injection)
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("users.db")

        # ❌ UNSAFE QUERY
        query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"

        conn.execute(query)
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# ❌ VULNERABLE LOGIN (SQL Injection)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("users.db")

        # ❌ UNSAFE QUERY
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

        result = conn.execute(query).fetchone()
        conn.close()

        if result:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return "Invalid Credentials"

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
    app.run(debug=True)
