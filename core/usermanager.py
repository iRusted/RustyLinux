
import re
import platform
import subprocess
from pathlib import Path


SYSTEM = platform.system()

HOME_BASE = Path("/home") if SYSTEM == "Linux" else Path("C:/Users")


def validate_username(username: str) -> str | None:
    """Normalize and validate a Linux username."""

    if not isinstance(username, str) or not username.strip():
        return None

    username = username.lower()
    username = re.sub(r"[^a-z0-9_-]", "", username)

    if not username:
        return None

    if not username[0].isalpha() and username[0] != "_":
        username = f"user_{username}"

    return username[:24]

    return username[:24]


def user_exists(username: str) -> bool:
    """Check whether a user exists on the current OS."""

    if SYSTEM == "Linux":
        import pwd

        try:
            pwd.getpwnam(username)
            return True
        except KeyError:
            return False

    elif SYSTEM == "Windows":
        import win32net

        try:
            win32net.NetUserGetInfo(None, username, 1)
            return True
        except Exception as error:
            # ERROR_NONE_MAPPED / ERROR_NO_SUCH_USER
            if getattr(error, "winerror", None) in (2221, 1332):
                return False
            raise

    raise OSError(f"Unsupported operating system: {SYSTEM}")


def get_available_username(username: str) -> str | None:
    """Find an available username."""

    base = validate_username(username)

    if base is None:
        return None

    candidate = base
    counter = 1

    while user_exists(candidate):
        suffix = str(counter)
        candidate = f"{base[:24 - len(suffix)]}{suffix}"
        counter += 1

    return candidate


def create_linux_user(username: str) -> dict:
    """Create a Linux account and its home directory."""

    if SYSTEM != "Linux":
        return {
            "success": False,
            "error": "Linux account creation is unavailable on this OS."
        }

    available_username = get_available_username(username)

    if available_username is None:
        return {
            "success": False,
            "error": "Invalid username"
        }

    try:
        subprocess.run(
            [
                "useradd",
                "-m",
                "-s", "/bin/bash",
                available_username
            ],
            capture_output=True,
            text=True,
            check=True
        )

        return {
            "success": True,
            "username": available_username,
            "home_dir": str(HOME_BASE / available_username)
        }

    except subprocess.CalledProcessError as error:
        return {
            "success": False,
            "error": error.stderr.strip()
        }


def create_windows_user(username: str) -> dict:
    """Create a Windows local account."""

    if SYSTEM != "Windows":
        return {
            "success": False,
            "error": "Windows account creation is unavailable on this OS."
        }

    import win32net

    available_username = get_available_username(username)

    if available_username is None:
        return {
            "success": False,
            "error": "Invalid username"
        }

    try:
        user_info = {
            "name": available_username,
            "password": None,
            "priv": 1,
            "flags": 0x10000,  # UF_PASSWD_NOTREQD
            "comment": "RustyLinux managed account"
        }

        win32net.NetUserAdd(None, 1, user_info)

        return {
            "success": True,
            "username": available_username,
            "home_dir": str(HOME_BASE / available_username)
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }
