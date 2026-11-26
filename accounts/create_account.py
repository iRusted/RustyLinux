from core.usermanager import create_linux_user
from database.database_handler import add_user

def create_account(discord_id, discord_username):
    linux_user = create_linux_user(discord_username)

    if not linux_user["success"]:
        return "Linux account creation failed."

    user_id = add_user(
        discord_id,
        linux_user["username"],
        linux_user["home_dir"]
    )

    if user_id is None:
        return "Database registration failed."

    return "Account created successfully."