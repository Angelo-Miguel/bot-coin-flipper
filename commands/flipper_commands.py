from discord import app_commands
from discord.ext import commands
import discord
import random

from utils.logger import get_logger

logger = get_logger("commands")


class FlipperCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="flip", description="Separe os itens com vírgula e espaço (, )"
    )
    async def flip(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer()
        itens = query.split(", ")
        logger.info(itens)

        selected_item = random.choice(itens)
        await interaction.followup.send(selected_item)
        logger.info(selected_item)
