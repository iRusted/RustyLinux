from core.usermanager import create_linux_user
from core.usermanager import create_windows_user
from database.database_handler import add_user, get_user
import platform

def create_account(discord_id, discord_username):
    if get_user(discord_id) is not None:
        return "Account already created."

    if platform.system() == "Linux":
        account = create_linux_user(discord_username)
    elif platform.system() == "Windows":
        account = create_windows_user(discord_username)
    else:
        account = {
            "success": False,
            "error": "Unsupported operating system."
        }

    if not account["success"]:
        return "Account creation failed."

    user_id = add_user(
        discord_id,
        account["username"],
        account["home_dir"]
    )

    if user_id is None:
        return "Database registration failed."

    return "Account created successfully."