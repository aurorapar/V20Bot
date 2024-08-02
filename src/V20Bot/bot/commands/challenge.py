import random

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Bot

from ...character import Ability, Attribute


class Challenge(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(description="Creates a challenge you want a player to respond to")
    @app_commands.allowed_contexts(guilds=True)
    @app_commands.describe(
        player='The player you wish to take part in the challenge',
        attribute='The attribute for the challenge',
        ability='The ability (talent, skill, knowledge) for the challenge',
        hidden='Do you want to hide this from the server?'
    )
    @app_commands.choices(attribute=[
        app_commands.Choice(name=attribute, value=attribute) for attribute in random.choices(list(Attribute), k=25)
    ])
    @app_commands.choices(ability=[
        app_commands.Choice(name=ability, value=ability) for ability in random.choices(list(Ability), k=25)
    ])
    async def challenge(self, interaction: discord.Interaction, player: discord.Member, attribute: str, ability: str,
                        hidden: bool = True):
        challenge_creator = interaction.user

