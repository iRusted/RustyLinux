from bot.bot_config import bot, token

@bot.event
async def on_ready():
    print(f"Bot is running as {bot.user}")

bot.run(token)