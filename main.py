from bot.bot_config import bot, token
from bot.error_handler import on_app_command_error

bot.tree.on_error = on_app_command_error










@bot.event
async def on_ready():
    print(f"Bot is running as {bot.user}")



bot.run(token)