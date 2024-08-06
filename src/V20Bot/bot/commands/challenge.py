import random

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Bot

from ...character import Ability, Attribute
from ..event_handlers import get_player_dicepool

attribute_choices = list(Attribute)
while len(attribute_choices) > 25:
    attribute_choices.remove(random.choice(attribute_choices))
ability_choices = list(Ability)
while len(ability_choices) > 25:
    ability_choices.remove(random.choice(ability_choices))


class Challenge(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(description="Creates a challenge you want a player to respond to")
    @app_commands.allowed_contexts(guilds=True)
    @app_commands.describe(
        player='The player you wish to take part in the challenge',
        attribute='The attribute for the challenge',
        ability='The ability (talent, skill, knowledge) for the challenge',
        action='Describe the action you\'re taking (in quotes, like "Punching you")',
        hidden='Do you want to hide this from the server?'
    )
    @app_commands.choices(attribute=[app_commands.Choice(name=attribute, value=attribute) for attribute in attribute_choices])
    @app_commands.choices(ability=[app_commands.Choice(name=ability, value=ability) for ability in ability_choices])
    async def challenge(self, interaction: discord.Interaction, player: discord.Member, attribute: str, ability: str,
                        action: str, hidden: bool = True):
        aggressor_dicepool = await get_player_dicepool(interaction)

