import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

def run_cmd_admin(commands):
    batch_script_path = os.path.join(os.getcwd(), 'dependencies_Deletion.bat')
    with open(batch_script_path, 'w') as batch_file:
        batch_file.write("@echo off\n")
        for command in commands:
            batch_file.write(f'{command}\n')
        batch_file.write("pause")

    subprocess.run(['runas', '/user:Administrator', batch_script_path], shell=True)

def service_is_installed_check(service_name):
    try:
        result = subprocess.run(['sc', 'query', service_name], capture_output=True, text=True)
        if "does not exist" in result.stderr:
            return False
        return True
    except Exception as e:
        print(f"Error while checking installed services {service_name}: {e}")
        return False
#STEPS
def step_0_execute():
    root = tk.Tk()
    root.withdraw()

    user_response = messagebox.askokcancel("Confirmation", "Vanguard dependencies will be removed, and your computer "
                                                           "will restart. After the restart, please reopen this "
                                                           "program to complete the process.")
    if user_response:
        commands = [
            "sc delete vgc",
            "sc delete vgk"
        ]
        run_cmd_admin(commands)

        p = subprocess.Popen(["powershell.exe", "Restart-Computer -Force"],
                             stdout=sys.stdout)
        p.communicate()
    else:
        print("Program is closed.")
        exit(0)

def step_1_execute():
    root = tk.Tk()
    root.withdraw()

    user_response = messagebox.askokcancel("Confirmation", "Vanguard folder will be deleted. You can restart "
                                                           "LOL-Client and start the Updateprocess. Have fun!")
    if user_response:
        command = "Remove-Item -Path 'C:\\Program Files\\Riot Vanguard' -Recurse -Force;"
        run_cmd_admin(command)
    else:
        print("Program is closed.")
#MAIN
def main():
    services = ["vgc", "vgk"]
    for service in services:
        if service_is_installed_check(service):
            step_0_execute()
        else:
            step_1_execute()


if __name__ == "__main__":
    main()
