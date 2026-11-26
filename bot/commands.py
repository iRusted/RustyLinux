import discord 
from discord.ext import commands
from core.executor import run_command
from bot.bot_config import bot
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