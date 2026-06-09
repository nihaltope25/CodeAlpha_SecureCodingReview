import os

# Hardcoded password
password = "admin123"

def login(user_input):
    if user_input == password:
        print("Access Granted")
    else:
        print("Access Denied")

# Command injection risk
def run_command(cmd):
    os.system(cmd)

user = input("Enter password: ")
login(user)

command = input("Enter command: ")
run_command(command)