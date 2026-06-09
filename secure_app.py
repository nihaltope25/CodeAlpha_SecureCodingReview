import subprocess
import getpass

# Secure password handling
def login():
    user_input = getpass.getpass("Enter password: ")
    if user_input == "admin123":
        print("Access Granted")
    else:
        print("Access Denied")

# Safe command execution
def run_command(cmd):
    allowed_commands = ["dir", "whoami", "echo"]
    if cmd in allowed_commands:
        subprocess.run(cmd, shell=True)
    else:
        print("Command not allowed")

login()

command = input("Enter safe command: ")
run_command(command)