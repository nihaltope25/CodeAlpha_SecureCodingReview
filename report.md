# Secure Coding Review Report

## 👤 Author

**Name:** Nihal Tope (Intern- Code Alpha)

## 🔢 Version

1.0

---

## 📌 Overview

This project demonstrates the identification and mitigation of security vulnerabilities in a Python application using static code analysis tools.

---

## 🛠️ Tools & Technologies

* Python 3.13
* Bandit (Static Code Analysis Tool)
* Windows OS

---

## 🔍 Vulnerabilities Identified

| Vulnerability      | Severity | Status  |
| ------------------ | -------- | ------- |
| Hardcoded Password | Low      | Fixed  |
| Command Injection  | High     | Fixed  |

---

## ⚠️ Issue Details

### 1. Hardcoded Password

* Description: Password stored directly in source code
* Risk: Exposure leads to unauthorized access

### 2. Command Injection

* Description: Unsafe use of `os.system()`
* Risk: Execution of malicious commands

---

## 🔄 Code Improvement

### Before (Vulnerable Code)

```
os.system(cmd)
```

### After (Secure Code)

```
subprocess.run(cmd, shell=True)
```

---

## 🔧 Remediation Steps

* Removed hardcoded credentials
* Used secure input handling (`getpass`)
* Restricted command execution
* Replaced unsafe system calls

---

## 🎯 Learning Outcomes

* Understanding of secure coding practices
* Experience with vulnerability scanning tools
* Knowledge of command injection risks

---

## 🚀 How to Run
      python -m bandit vulnerable_app.py

---      

## 📢 Conclusion

This project successfully identified and mitigated security vulnerabilities, improving the application’s safety and reliability through secure coding practices.

