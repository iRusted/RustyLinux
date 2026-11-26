import discord
from discord import app_commands

import traceback
import io


# =====================================================
# APPLICATION COMMAND ERROR HANDLING
# =====================================================
    
async def on_app_command_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
):
    original_error = getattr(error, "original", error)

    traceback_text = "".join(
        traceback.format_exception(
            type(original_error),
            original_error,
            original_error.__traceback__
        )
    )

    # Log the full traceback locally
    print(traceback_text)

    message = (
        "❌ **Command failed**\n"
        f"Error: `{type(original_error).__name__}`"
    )

    try:
        if interaction.response.is_done():
            await interaction.followup.send(message)
        else:
            await interaction.response.send_message(message)

    except discord.NotFound:
        print("Interaction expired before the error message could be sent.")

    except discord.HTTPException as e:
        print(f"Failed to send error message: {e}")
