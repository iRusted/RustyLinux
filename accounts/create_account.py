from database.database_handler import add_user, get_user

def create_user(username, discord_id):

    existing_user = get_user(discord_id)

    if existing_user is not None:
        return "Account Already Created"

    try:
        user_id = add_user(discord_id, username)

        if user_id is None:
            return "Account Creation Failed"

    except Exception as error:
        print(f"Failed to create user: {error}")
        return "Account Creation Failed"

    return "Account Created"