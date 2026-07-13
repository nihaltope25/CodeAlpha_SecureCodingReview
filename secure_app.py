from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "super_secure_key"

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

app.config['MAX_LOGIN_ATTEMPTS'] = 5

@app.route("/")
def home():
    return render_template("index.html")

# ✅ SECURE REGISTER (Parameterized Query)
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("users.db")

        # ✅ SAFE QUERY
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# ✅ SECURE LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # 🔒 Brute-force protection
        if 'login_attempts' in session and session['login_attempts'] >= app.config['MAX_LOGIN_ATTEMPTS']:
            return "Account locked. Try later."

        conn = sqlite3.connect("users.db")

        # ✅ SAFE QUERY
        result = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()

        conn.close()

        if result:
            session['user'] = username
            session['login_attempts'] = 0
            return redirect("/dashboard")
        else:
            session['login_attempts'] = session.get('login_attempts', 0) + 1
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
