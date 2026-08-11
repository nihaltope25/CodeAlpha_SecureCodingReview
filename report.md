# Secure Coding Review Report

## 👤 Author

**Name:** Nihal Tope (Intern - CodeAlpha)

## 🔢 Version

1.1

---

## 📌 Overview

This project demonstrates the identification and mitigation of common security vulnerabilities in a Python Flask application. The vulnerable version is reviewed and then improved using safer coding practices.

---

## 🛠️ Tools & Technologies

* Python 3.13
* Flask
* SQLite
* Bandit (Static Code Analysis Tool)
* Windows OS

---

## 🔍 Vulnerabilities Identified

| Vulnerability | Severity | Status |
| --- | --- | --- |
| Hardcoded Secret Key | Medium | Improved |
| SQL Injection | High | Fixed |
| Plain-Text Password Storage | High | Fixed |
| Debug Mode Enabled | Medium | Fixed |

---

## ⚠️ Issue Details

### 1. SQL Injection

* **Description:** User input was directly inserted into SQL queries using string formatting.
* **Risk:** A malicious input could modify the SQL statement and affect database operations.
* **Fix:** Parameterized SQL queries are used in the secure version.

### 2. Plain-Text Password Storage

* **Description:** Passwords were stored directly in the SQLite database.
* **Risk:** Anyone gaining access to the database could read the stored passwords.
* **Fix:** Passwords are hashed before storage and verified using a password-hashing function.

### 3. Hardcoded Secret Key

* **Description:** The Flask session secret was written directly in the source code.
* **Risk:** Exposing the key could allow session-related security issues.
* **Fix:** The secure version reads the secret key from an environment variable.

### 4. Debug Mode

* **Description:** Flask debug mode was enabled in the application.
* **Risk:** Debug information can expose sensitive application details.
* **Fix:** Debug mode is disabled when running the application.

---

## 🔄 Code Improvement

### Before (Vulnerable Code)

```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

### After (Secure Code)

```python
result = conn.execute(
    "SELECT id, username, password_hash FROM users WHERE username = ?",
    (username,)
).fetchone()
```

The secure version uses parameterized queries and verifies a hashed password instead of placing user input directly into SQL statements.

---

## 🔧 Remediation Steps

* Replaced dynamically constructed SQL queries with parameterized queries.
* Added password hashing using Werkzeug.
* Added password verification during login.
* Moved the Flask secret key to an environment variable.
* Added basic login-attempt protection.
* Disabled Flask debug mode for normal execution.

---

## 🎯 Learning Outcomes

* Understanding of secure coding practices.
* Experience with static code analysis using Bandit.
* Understanding of SQL injection risks.
* Understanding of password storage and authentication security.
* Experience improving a vulnerable Python Flask application.

---

## 🚀 How to Run

Install the required packages:

```bash
pip install flask werkzeug
```

Run the secure application:

```bash
python secure_app.py
```

To scan the vulnerable application with Bandit:

```bash
python -m bandit vulnerable_app.py
```

---

## 📢 Conclusion

This project demonstrates how common security weaknesses can be identified and addressed through secure coding practices. The comparison between the vulnerable and secure versions shows the importance of parameterized queries, password hashing, secure configuration, and safe application settings.