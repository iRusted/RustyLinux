import discord
import os
from pathlib import Path
from dotenv import load_dotenv
from discord.ext import commands

ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_PATH)

def get_token():
    return os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

token = get_token()

if not token:
    raise RuntimeError("BOT_TOKEN could not be loaded!")

current_bot_host = "iRustedzz"

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)