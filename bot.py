from core.bot_client import FlipperBot
from config import Config

bot = FlipperBot()

bot.run(Config.DISCORD_TOKEN)
