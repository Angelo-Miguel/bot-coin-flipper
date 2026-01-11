import discord
from discord.ext import commands
from utils.logger import get_logger

logger = get_logger("bot")


class FlipperBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents, aplication_id=None)

    async def setup_hook(self):
        from commands.flipper_commands import FlipperCommands

        await self.add_cog(FlipperCommands(self))
        await self.tree.sync()

    async def on_ready(self):
        logger.info("bot conectado como %s", self.user)
