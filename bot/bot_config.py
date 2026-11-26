import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from discord.ext import tasks

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

token = BOT_TOKEN # Discord Bot Token

current_bot_host = "iRustedzz" # Change if self hosting

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)