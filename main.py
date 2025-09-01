import ctypes
import subprocess
from tkinter import messagebox

#pip install pyinstaller
#python -m PyInstaller --name VanguardKiller --onefile --manifest=VanguardKiller.exe.manifest main.py

def main():
    """
    Entry point of the program.

    Returns:
        None
    """
    if is_service_installed("vgc") or is_service_installed("vgk"):
        step_0_execute()
    else:
        step_1_execute()


def step_0_execute():
    """
    Stops and removes Vanguard services after user confirmation
    and restarts the system.

    Displays a confirmation dialog. If the user accepts, the function:
    - Stops Vanguard services (vgc and vgk)
    - Kills the vgtray.exe process
    - Deletes the Vanguard services
    - Restarts the computer

    If the user cancels, the program prints a closing message and exits.
    """
    user_response = messagebox.askokcancel("Confirmation",
                                           "Vanguard dependencies will be removed, Vanguard will be uninstalled, "
                                           "and your computer will restart.\n\n"
                                           "After the restart, please reopen this program to complete the process."
                                           )
    if user_response:

        commands = [
            "echo Stop services...",
            "timeout /t 2 /nobreak >nul",
            "sc stop vgc",
            "sc stop vgk",
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
    """
    Deletes the Vanguard folder after user confirmation.

    If the user accepts, the function:
    - Kills the vgtray.exe process
    - Deletes the 'Riot Vanguard' folder
    - Closes the program

    If declined, the program prints a closing message and exits.
    """
    user_response = messagebox.askokcancel("Confirmation",
                                           "The Vanguard folder will be deleted.\n\n"
                                           "Afterwards, restart the League of Legends client to start the update process.\n\n"
                                           "Have fun!"
                                           )
    if user_response:
        commands = [
            "echo Kill vgtray.exe, the program behind Vortex...",
            "timeout /t 2 /nobreak >nul",
            "taskkill /f /im vgtray.exe",
            "timeout /t 2 /nobreak >nul",
            "echo Delete 'Riot Vanguard'-folder...",
            "rmdir /s /q \"C:\\Program Files\\Riot Vanguard\"",
            "timeout /t 2 /nobreak >nul",
            "echo Finished! Closing...",
            "timeout /t 4 /nobreak >nul",
            "exit"
        ]
        run_cmd_admin(commands)
    else:
        print("Program is closed.")


def run_cmd_admin(commands):
    """
    Runs a list of commands in an elevated command prompt.

    Joins the provided commands and executes them with administrator privileges using cmd.exe.
    """
    # noinspection PyUnresolvedReferences
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", "cmd.exe", "/k " + " & ".join(commands), None, 1
    )

def is_service_installed(service_name):
    """
    Checks if a Windows service with the given name exists.

    Runs 'sc query' for the service. Returns True if the service exists (running or stopped),
    otherwise False.
    """
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


if __name__ == "__main__":
    main()
