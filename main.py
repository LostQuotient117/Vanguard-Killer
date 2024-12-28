import json
import os
import subprocess, sys

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
    p = subprocess.Popen(["powershell.exe", "C:\\Users\\Jannick.Gottschalk\\IdeaProjects\\Vanguard Killer\\step_0.ps1"],
                         stdout=sys.stdout)
    p.communicate()


def main():
    state = load_checkpoint()
    if state is None:
        state = {"step": 0}
        save_checkpoint(state)
        step_0_execute()


if __name__ == "__main__":
    main()
