import os
import subprocess
import sys
import time
import tkinter as tk
from tkinter import messagebox, ttk


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
            ['wmic', 'product', 'where', f'name="{program_name}"', 'call', 'uninstall'],
            #TODO: ACHTUNG!!! Nicht ausführen. Braucht Admin-Berechtigung ohne Passwort eingeben zu müssen.
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

def update_progress(progress, value):
    progress['value'] = value
    progress.update_idletasks()


#STEPS
def step_0_execute():
    root = tk.Tk()
    root.withdraw()

    user_response = messagebox.askokcancel("Confirmation", "Vanguard dependencies will be removed, vanguard will be "
                                                           "deinstalled, and your computer will restart."
                                                           " After the restart, please reopen this "
                                                           "program to complete the process.")
    if user_response:

        progress_window = tk.Toplevel(root)
        progress_window.title("Progress")
        progress = ttk.Progressbar(progress_window, orient="horizontal", length=200, mode="determinate")
        progress.pack(pady=20)
        progress["maximum"] = 100

        commands = [
            "sc delete vgc",
            "sc delete vgk"  #TODO: Er scheint den zweiten Dienst nicht ordentlich zu deinstallieren
        ]
        update_progress(progress, 20)
        time.sleep(0.5)
        run_cmd_admin(commands)
        update_progress(progress, 60)
        time.sleep(0.5)
        uninstall_program("Riot Vanguard")
        update_progress(progress, 100)
        time.sleep(1)
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
        progress_window = tk.Toplevel(root)
        progress_window.title("Progress")
        progress = ttk.Progressbar(progress_window, orient="horizontal", length=200, mode="determinate")
        progress.pack(pady=20)
        progress["maximum"] = 100

        update_progress(progress, 20)
        command = "Remove-Item -Path 'C:\\Program Files\\Riot Vanguard' -Recurse -Force;"
        update_progress(progress, 60)
        time.sleep(0.5)
        run_cmd_admin(command)
        update_progress(progress, 100)
        time.sleep(0.5)
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
