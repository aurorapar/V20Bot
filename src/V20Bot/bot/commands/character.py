import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Bot

from ..event_handlers.display_character import display_character


class Character(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(description="View your cahracter sheet stats")
    @app_commands.allowed_contexts(guilds=True)
    @app_commands.describe(
    )
    async def character(self, interaction: discord.Interaction):
        await display_character(interaction)
