import discord
from discord.ext import commands
from bot.bot_config import bot
from bot.bot_config import token
from bot.error_handler import on_app_command_error

bot.tree.on_error = on_app_command_error

@bot.tree.command(name="ping", description="Check your ping AND if the bot is online")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Pong! {round(bot.latency * 1000)}ms"
    )








@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is running as {bot.user}")



bot.run(token)