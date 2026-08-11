# CodeAlpha Secure Coding Review

A simple Python Flask project demonstrating how common web application security issues can be identified and improved through secure coding practices.

## Project Overview

The repository contains two versions of a small Flask login application:

- `vulnerable_app.py` — intentionally demonstrates unsafe SQL query construction.
- `secure_app.py` — improves the application using parameterized SQL queries, password hashing, safer configuration, and basic login-attempt protection.
- `report.md` — documents the vulnerabilities, remediation steps, and learning outcomes.

## Security Issues Covered

- SQL Injection
- Plain-text password storage
- Hardcoded application secrets
- Flask debug mode
- Basic brute-force protection

## Tools & Technologies

- Python 3.13
- Flask
- SQLite
- Werkzeug
- Bandit
- Windows OS

## Installation

Install the required packages:

```bash
pip install flask werkzeug bandit
```

## Run the Secure Version

Set a secret key before running the application.

Windows PowerShell:

```powershell
$env:FLASK_SECRET_KEY="your-random-secret-key"
python secure_app.py
```

The application will start locally using Flask.

## Run Bandit

To scan the intentionally vulnerable application:

```bash
python -m bandit vulnerable_app.py
```

## Important Note

`vulnerable_app.py` is intentionally insecure for educational comparison. It should only be used in a controlled local environment and should not be deployed publicly.

## Author

Nihal Tope — CodeAlpha Cyber Security Intern