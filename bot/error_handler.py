import discord 
from discord.ext import commands
from discord import app_commands
from discord.ext import tasks
from bot_config import bot, intents


@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
):
    import traceback
    import io

    tb = "".join(
        traceback.format_exception(
            type(error),
            error,
            error.__traceback__
        )
    )

    file = discord.File(
        io.BytesIO(tb.encode("utf-8")),
        filename="traceback.txt"
    )

    message = (
        f"❌ **Command failed**\n"
        f"Error: `{type(error).__name__}`"
    )

    try:
        if interaction.response.is_done():
            await interaction.followup.send(
                message,
                file=file
            )
        else:
            await interaction.response.send_message(
                message,
                file=file
            )

    except discord.NotFound:
        # Interaction expired before we could respond.
        print("Interaction expired before the error message could be sent.")
        print(tb)

    except discord.HTTPException as e:
        print(f"Failed to send error message: {e}")
        print(tb)

@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
):
    import traceback
    import io

    tb = "".join(
        traceback.format_exception(
            type(error),
            error,
            error.__traceback__
        )
    )

    file = discord.File(
        io.BytesIO(tb.encode("utf-8")),
        filename="traceback.txt"
    )

    message = (
        f"❌ **Command failed**\n"
        f"Error: `{type(error).__name__}`"
    )

    try:
        if interaction.response.is_done():
            await interaction.followup.send(
                message,
                file=file
            )
        else:
            await interaction.response.send_message(
                message,
                file=file
            )

    except discord.NotFound:
        # Interaction expired before we could respond.
        print("Interaction expired before the error message could be sent.")
        print(tb)

    except discord.HTTPException as e:
        print(f"Failed to send error message: {e}")
        print(tb)
#def build_message_embed(data) -> discord.Embed:
