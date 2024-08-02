import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Bot

from ..event_handlers import set_character_image


class SetCharacterImage(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.allowed_contexts(guilds=True)
    @app_commands.describe(
        link="The link of your character image. Don't user imgur, they don't like Discord. Try https://postimg.cc"
    )
    async def setcharacterimage(self, interaction: discord.Interaction, link: str):
        await set_character_image(interaction, link)
