
import discord
from bot.bot_config import bot, token
from bot.error_handler import on_app_command_error
from bot.commands import run_command_test, ping 
from core.executor import run_command

bot.tree.on_error = on_app_command_error


@bot.tree.command(
    name="ping",
    description="Check your ping AND if the bot is online"
)
async def cmd_ping(interaction: discord.Interaction):
    await ping(interaction)


@bot.tree.command(
    name="run_command_test",
    description="Test Command"
)
async def cmd_test_command(
    interaction: discord.Interaction,
    command: str
):
    await run_command_test(interaction, command)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is running as {bot.user}")


bot.run(token)
