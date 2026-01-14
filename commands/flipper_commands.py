from discord import app_commands
from discord.ext import commands
import discord
import random

from utils.logger import get_logger

logger = get_logger("commands")


class ReflipView(discord.ui.View):
    def __init__(
        self, items: list[str], author: discord.User, *, timeout: float = None
    ):
        super().__init__(timeout=timeout)
        self.items = items
        self.author = author
        self.flips = 1

    @discord.ui.button(label="Reflip", style=discord.ButtonStyle.primary, emoji="🔁")
    async def reflip(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user != self.author:
            await interaction.response.send_message(
                "Apenas quem pediu pode reflipar.", ephemeral=True
            )
            return

        selected_item = random.choice(self.items)
        self.flips += 1
        logger.info("reflip by %s -> %s", interaction.user, selected_item)

        # Atualiza o embed
        items_list = "\n".join(
            f"**{i} - ** {v}" for i, v in enumerate(self.items, start=1)
        )
        embed = discord.Embed(
            title="🪙 Flip — Resultado",
            description="Aqui estão os itens e o resultado:",
            color=discord.Color.dark_purple(),
        )
        embed.add_field(name="Itens", value=items_list, inline=False)
        embed.add_field(name="Escolhido", value=f"**{selected_item}**", inline=False)

        icon_url = None
        try:
            icon_url = interaction.user.display_avatar.url
        except Exception:
            icon_url = None

        embed.set_footer(
            text=f"Pedido por {self.author} • Flip #{self.flips}", icon_url=icon_url
        )

        await interaction.response.edit_message(embed=embed, view=self)


class FlipperCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="flip", description="Separe os itens com vírgula e espaço (, )"
    )
    async def flip(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer()
        # Normaliza e remove itens vazios
        items = [item.strip() for item in query.split(",") if item.strip()]
        logger.info("flip items: %s", items)

        if not items:
            await interaction.followup.send(
                "Nenhum item válido fornecido. Separe os itens com vírgula (ex: `maçã, banana, laranja`).",
                ephemeral=True,
            )
            return

        # Seleciona um item aleatorio
        selected_item = random.choice(items)
        logger.info("flip selected: %s", selected_item)

        # Monta a lista numerada
        items_list = "\n".join(f"**{i} - ** {v}" for i, v in enumerate(items, start=1))

        # Constrói o embed
        embed = discord.Embed(
            title="🪙 Flip — Resultado",
            description="Aqui estão os itens e o resultado:",
            color=discord.Color.dark_purple(),
        )
        embed.add_field(name="Itens", value=items_list, inline=False)
        embed.add_field(name="Escolhido", value=f"**{selected_item}**", inline=False)

        # Tenta pegar avatar do usuário para o footer
        icon_url = None
        try:
            icon_url = interaction.user.display_avatar.url
        except Exception:
            icon_url = None

        embed.set_footer(
            text=f"Pedido por {interaction.user} • Flip #1", icon_url=icon_url
        )

        # Cria a view
        view = ReflipView(items, interaction.user)
        await interaction.followup.send(embed=embed, view=view)
