import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

#pyinstaller --name VanguardKiller --onefile main.py
def run_cmd_admin(commands):
    batch_script_path = os.path.join(os.getcwd(), 'dependencies_Deletion.bat')
    with open(batch_script_path, 'w') as batch_file:
        batch_file.write("@echo off\n")
        for command in commands:
            batch_file.write(f'{command}\n')
        batch_file.write("pause")

    subprocess.run(['runas', '/user:Administrator', batch_script_path], shell=True)

def is_service_installed(service_name):
    try:
        result = subprocess.run(['sc', 'query', service_name], capture_output=True, text=True)

        if result.returncode == 1060:
            return False

        for line in result.stdout.splitlines():
            if "STATE" in line:
                parts = line.split("STATE")[1].strip().split()
                if len(parts) > 1:
                    state_code = parts[1].strip(":")
                    if state_code == "4":  # RUNNING
                        return True
                    elif state_code == "1":  # STOPPED
                        return False
        return False
    except Exception as e:
        print(f"Error while checking service {service_name}: {e}")
        return False

def uninstall_program(program_name):
    try:
        result = subprocess.run(
            ['wmic', 'product', 'where', f'name="{program_name}"', 'call', 'uninstall'], #TODO: ACHTUNG!!! Nicht ausführen. Braucht Admin-Berechtigung ohne Passwort eingeben zu müssen.
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"The program '{program_name}' was successfully deinstalled.")
        else:
            print(f"Error at uninstalling'{program_name} or it was not found.': {result.stderr}")
    except Exception as e:
        print(f"An Error occurred: {e}")

def restart_computer():
    p = subprocess.Popen(["powershell.exe", "Restart-Computer -Force"],
                         stdout=sys.stdout)
    p.communicate()
#STEPS
def step_0_execute():
    root = tk.Tk()
    root.withdraw()

    user_response = messagebox.askokcancel("Confirmation", "Vanguard dependencies will be removed, vanguard will be "
                                                           "deinstalled, and your computer will restart."
                                                           " After the restart, please reopen this "
                                                           "program to complete the process.")
    if user_response:
        commands = [
            "sc delete vgc",
            "sc delete vgk" #TODO: Er scheint den zweiten Dienst nicht ordentlich zu deinstallieren
        ]
        run_cmd_admin(commands)
        uninstall_program("Riot Vanguard")
        restart_computer()
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
    servicevgc = "vgc"
    servicevgk = "vgk"
    if is_service_installed(servicevgc) or is_service_installed(servicevgk):
        step_0_execute()
    else:
        step_1_execute()


if __name__ == "__main__":
    main()
