from discord import app_commands
from discord.ext import commands
import discord
import random

from utils.logger import get_logger

logger = get_logger("commands")


# Modal para editar a query
class EditQueryModal(discord.ui.Modal, title="Editar query"):
    query = discord.ui.TextInput(
        label="Query (itens separados por vírgula)",
        style=discord.TextStyle.long,
        default="",  # será setado no __init__
        max_length=4000,
    )

    def __init__(self, view: "ReflipView"):
        super().__init__()
        self.view = view
        self.query.default = view.raw_query  # preenche o campo

    async def on_submit(self, interaction: discord.Interaction):
        new_query = self.query.value
        old_query = self.view.raw_query

        items = [i.strip() for i in new_query.split(",") if i.strip()]
        if not items:
            await interaction.response.send_message(
                "Query inválida — envie itens separados por vírgula.", ephemeral=True
            )
            return

        # Atualiza a view e o embed
        self.view.items = items
        self.view.raw_query = new_query
        self.view.flips = 1
        selected = random.choice(items)

        logger.info(
            "query edited by %s | before=%r | after=%r | selected=%s",
            interaction.user,
            old_query,
            new_query,
            selected,
        )

        items_list = "\n".join(f"**{i} -** {v}" for i, v in enumerate(items, start=1))
        embed = discord.Embed(
            title="🪙 Flip — Resultado",
            description="Query editada:",
            color=discord.Color.dark_purple(),
        )
        embed.add_field(name="Itens", value=items_list, inline=False)
        embed.add_field(name="Escolhido", value=f"**{selected}**", inline=False)
        embed.set_footer(
            text=f"Pedido por {self.view.author} • Flip #1",
            icon_url=(
                getattr(self.view.author, "display_avatar", None).url
                if getattr(self.view.author, "display_avatar", None)
                else None
            ),
        )

        # Edita a mensagem original (certifique-se que view.message foi setada)
        if hasattr(self.view, "message") and self.view.message:
            await self.view.message.edit(embed=embed, view=self.view)
            await interaction.response.send_message("Query atualizada.", ephemeral=True)
        else:
            await interaction.response.send_message(
                "Não foi possível atualizar a mensagem (message não encontrada).",
                ephemeral=True,
            )


class ReflipView(discord.ui.View):
    def __init__(
        self,
        items: list[str],
        author: discord.User,
        raw_query: str,
        *,
        timeout: float = None,
    ):
        super().__init__(timeout=timeout)
        self.items = items
        self.author = author
        self.raw_query = raw_query
        self.flips = 1

    @discord.ui.button(label="Reflip", style=discord.ButtonStyle.primary, emoji="🔁")
    async def reflip(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user != self.author:
            logger.warning(
                "unauthorized reflip attempt | by=%s | owner=%s",
                interaction.user,
                self.author,
            )

            await interaction.response.send_message(
                "Apenas quem pediu pode reflipar.", ephemeral=True
            )
            return

        selected_item = random.choice(self.items)
        self.flips += 1
        logger.info(
            "reflip by %s: %s -> %s", interaction.user, self.items, selected_item
        )

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

    @discord.ui.button(
        label="Editar query", style=discord.ButtonStyle.success, emoji="✏️"
    )
    async def edit_query(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user != self.author:
            logger.warning(
                "unauthorized edit attempt | by=%s | owner=%s",
                interaction.user,
                self.author,
            )

            await interaction.response.send_message(
                "Apenas quem pediu pode editar.", ephemeral=True
            )
            return
        await interaction.response.send_modal(EditQueryModal(self))


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
        view = ReflipView(items=items, author=interaction.user, raw_query=query)
        msg = await interaction.followup.send(embed=embed, view=view)
        view.message = msg
