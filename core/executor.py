import subprocess
import shlex
import platform

def run_command(command: str):
    if not isinstance(command, str) or not command.strip():
        return subprocess.CompletedProcess(
            args=[],
            returncode=2,
            stdout="",
            stderr="No command was provided."
        )

    try:
        args = shlex.split(command, posix=platform.system() != "Windows")
    except ValueError as error:
        return subprocess.CompletedProcess(
            args=[command],
            returncode=2,
            stdout="",
            stderr=str(error)
        )

    if not args:
        return subprocess.CompletedProcess(
            args=[],
            returncode=2,
            stdout="",
            stderr="No command was provided."
        )

    try:
        return subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=30
        )
    except subprocess.TimeoutExpired as error:
        return subprocess.CompletedProcess(
            args=args,
            returncode=124,
            stdout=error.stdout or "",
            stderr=error.stderr or "Command timed out."
        )
    except (OSError, ValueError) as error:
        return subprocess.CompletedProcess(
            args=args,
            returncode=127,
            stdout="",
            stderr=str(error)
        )
