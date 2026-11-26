import discord 
from discord.ext import commands
from core.executor import run_command
from bot.bot_config import bot
from accounts.create_account import create_user
from database.database_handler import check_config
intents = discord.Intents.default()
intents.message_content = True

async def run_command_test( interaction: discord.Interaction, command: str):
    # Acknowledge the interaction before executing      
    await interaction.response.defer(ephemeral=True)

    # TODO: Resolve the Discord user to their authorized Linux account.
    username = interaction.user.name
    
    print(f"{username} has ran the command {command}!")

    result = run_command(command)

    output = result.stdout or result.stderr or "No output."

    await interaction.followup.send(
        f"Exit code: `{result.returncode}`\n"
        f"```text\n{output[:1800]}\n```"
    )

async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Pong! {round(bot.latency * 1000)}ms"
    )

async def new_user(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    
    register_status = check_config()
    
    if register_status == 0:
        await interaction.followup.send(
            "Registrations are closed! Please come again later. Check the Discord Server for Updates"
        )
        return None     

    username = interaction.user.name
    discord_id = interaction.user.id 
    
    result = create_user(username, discord_id)
    
    if result == "Account Created":
        await interaction.followup.send(
            f"Account has been created for <@{discord_id}>"
        )
    elif result == "Account Creation Failed":
        await interaction.followup.send(
            f"Account Creation Failed! Contact the Developer!"
        )
    elif result == "Account Already Created":
        await interaction.followup.send(
            f"Account Already Created for <@{discord_id}>"
        )
    