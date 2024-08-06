import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Bot

from ..event_handlers.import_sheet import import_sheet


class ImportSheet(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(description="Upload your character sheet for challenge automation")
    @app_commands.allowed_contexts(guilds=True)
    @app_commands.describe(
        pdf="Your sheet"
    )
    async def importsheet(self, interaction: discord.Interaction, pdf: discord.Attachment):
        await import_sheet(interaction, pdf)
