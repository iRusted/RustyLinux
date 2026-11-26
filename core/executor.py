import subprocess
import shlex

def run_command(command: str):
    result = subprocess.run(
        shlex.split(command),
        capture_output=True,
        text=True,
        timeout=30
    )

    return result
