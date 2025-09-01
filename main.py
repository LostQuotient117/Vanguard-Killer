import ctypes
import subprocess
from tkinter import messagebox

#pip install pyinstaller
#python -m PyInstaller --name VanguardKiller --onefile --manifest=VanguardKiller.exe.manifest main.py
def run_cmd_admin(commands):
    cmd_commands = " & ".join(commands)
    # noinspection PyUnresolvedReferences
    ctypes.windll.shell32.ShellExecuteW(
        None,"runas","cmd.exe",f"/k {cmd_commands}",None,1
    )

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
                        return True
                    else:
                        return False
        return False
    except Exception as e:
        print(f"Error while checking service {service_name}: {e}")
        return False


def update_progress(progress, value):
    progress['value'] = value
    progress.update_idletasks()


#STEPS
def step_0_execute():
    user_response = messagebox.askokcancel("Confirmation", "Vanguard dependencies will be removed, vanguard will be "
                                                           "deinstalled, and your computer will restart."
                                                           " After the restart, please reopen this "
                                                           "program to complete the process.")
    if user_response:

        commands = [
            "echo Stop services...",
            "timeout /t 2 /nobreak >nul",
            "sc stop vgc",
            "sc stop vgk"
            "timeout /t 2 /nobreak >nul",
            "echo Kill vgtray.exe, the program behind Vortex...",
            "taskkill /f /im vgtray.exe",
            "timeout /t 2 /nobreak >nul",
            "echo Delete Serices...",
            "sc delete vgc",
            "sc delete vgk",
            "echo Done. Restarting...",
            "timeout /t 4 /nobreak >nul",
            "shutdown /r /t 0"
        ]
        run_cmd_admin(commands)
    else:
        print("Program is closed.")
        exit(0)


def step_1_execute():
    user_response = messagebox.askokcancel("Confirmation", "Vanguard folder will be deleted. You can restart "
                                                           "LOL-Client and start the Updateprocess. Have fun!")
    if user_response:
        command = [
            "echo Kill vgtray.exe, the program behind Vortex...",
            "timeout /t 2 /nobreak >nul",
            "taskkill /f /im vgtray.exe",
            "timeout /t 2 /nobreak >nul",
            "echo Delete 'Riot Vanguard'-folder...",
            "rmdir /s /q \"C:\\Program Files\\Riot Vanguard\"",
            "timeout /t 2 /nobreak >nul",
            "echo Finished! Closing...",
            "timeout /t 2 /nobreak >nul",
            "exit"
            ]
        run_cmd_admin(command)
    else:
        print("Program is closed.")

#MAIN
def main():
    if is_service_installed("vgc") or is_service_installed("vgk"):
        step_0_execute()
    else:
        step_1_execute()


if __name__ == "__main__":
    main()
