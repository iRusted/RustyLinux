
import discord
from bot.bot_config import bot, token
from bot.error_handler import on_app_command_error
from core.executor import run_command

bot.tree.on_error = on_app_command_error


@bot.tree.command(name="ping", description="Check your ping AND if the bot is online"
)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Pong! {round(bot.latency * 1000)}ms"
    )


@bot.tree.command(name="run_command_test", description="Test Command")
async def run_command_test( interaction: discord.Interaction, command: str):
    # Acknowledge the interaction before executing
    await interaction.response.defer(ephemeral=True)

    # TODO: Resolve the Discord user to their authorized Linux account.
    username = None

    result = run_command(command)

    output = result.stdout or result.stderr or "No output."

    await interaction.followup.send(
        f"Exit code: `{result.returncode}`\n"
        f"```text\n{output[:1800]}\n```"
    )


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is running as {bot.user}")


bot.run(token)
