import json
import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

CHECKPOINT_FILE = "checkpoint.json"
step_0_Path = os.path.join(os.path.dirname(__file__), 'step_0.ps1')
log_file = "C:\\Git Repos\\Fehlermeldung.txt"


def save_checkpoint(data):
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(data, f)


def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            content = f.read().strip()
            if content:
                return json.loads(content)
            else:
                return None
    return None


def step_0_execute():
    root = tk.TK()
    root.withdraw()

    user_response = messagebox.askokcancel("Confirmation", "Vanguard dependencies will be removed, and your computer "
                                                           "will restart. After the restart, please reopen this "
                                                           "program to complete the process.")

    if user_response:
        commands = ("sc delete vgc;"
                    "")
        p = subprocess.Popen(["powershell.exe", "Restart-Computer -Force"],
                             stdout=sys.stdout)
        p.communicate()
    else:
        print("Program is closed.")


def main():
    state = load_checkpoint()
    if state is None:
        state = {"step": 0}
        save_checkpoint(state)
        step_0_execute()


if __name__ == "__main__":
    main()
