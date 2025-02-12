import json
import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

CHECKPOINT_FILE = "checkpoint.json"
step_0_Path = os.path.join(os.path.dirname(__file__), 'step_0.ps1')
log_file = "C:\\Git Repos\\Fehlermeldung.txt" #TODO: edit


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

def remove_dep(commands):
    batch_script_path = os.path.join(os.getcwd(), 'dependencies_Deletion.bat')
    with open(batch_script_path, 'w') as batch_file:
        batch_file.write("@echo off\n")
        for command in commands:
            batch_file.write(f'{command}\n')
        batch_file.write("pause")

    subprocess.run(['runas', '/user:Administrator', batch_script_path], shell=True)

def step_0_execute():
    root = tk.TK()
    root.withdraw()

    user_response = messagebox.askokcancel("Confirmation", "Vanguard dependencies will be removed, and your computer "
                                                           "will restart. After the restart, please reopen this "
                                                           "program to complete the process.")

    if user_response:
        commands = [
            "sc delete vgc",
            "sc delete vgk"
        ]
        remove_dep(commands)
        p = subprocess.Popen(["powershell.exe", "Restart-Computer -Force"],
                             stdout=sys.stdout)
        p.communicate()
    else:
        print("Program is closed.")

def step_1_execute():
    root = tk.TK()
    root.withdraw()

    user_response = messagebox.askokcancel("Confirmation", "Vanguard folder will be deleted. You can restart "
                                                           "LOL-Client and start the Updateprocess. Have fun!")
    if user_response:
        commands = "Remove-Item -Path 'C:\\Program Files\\Riot Vanguard' -Recurse -Force;" #TODO: def remove_vanguard_folder


def main():
    state = load_checkpoint() #TODO: more clean
    if state is None:
        state = {"step": 0}
        save_checkpoint(state) #TODO: find other Location for checkpoint
        step_0_execute()


if __name__ == "__main__":
    main()
