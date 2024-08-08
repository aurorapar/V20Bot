import random

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Bot

from ...character import Ability, Attribute, Discipline
from ..event_handlers import handle_challenge

attribute_choices = [attribute for attribute in Attribute]
while len(attribute_choices) > 25:
    attribute_choices.remove(random.choice(attribute_choices))
attribute_choices = set(attribute_choices)

ability_choices = [ability for ability in Ability]
while len(ability_choices) > 25:
    ability_choices.remove(random.choice(ability_choices))

discipline_choices = [discipline for discipline in Discipline]
while len(discipline_choices) > 25:
    discipline_choices.remove(random.choice(discipline_choices))


class Challenge(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(description="Creates a challenge you want a player to respond to")
    @app_commands.allowed_contexts(guilds=True)
    @app_commands.describe(
        player='The player you wish to take part in the challenge',
        attribute='The attribute for the challenge',
        ability='The ability (talent, skill, knowledge) for the challenge',
        discipline='Is there an applicable discipline you wish to use?',
        difficulty='The difficulty of the challenge',
        action='Describe the action you\'re taking (in quotes, like "Punching you")',
        hidden='Do you want to hide this from the server?'
    )
    @app_commands.choices(attribute=[app_commands.Choice(name=attribute, value=attribute) for attribute in attribute_choices])
    @app_commands.choices(ability=[app_commands.Choice(name=ability, value=ability) for ability in ability_choices])
    @app_commands.choices(ability=[app_commands.Choice(name=ability, value=ability) for ability in ability_choices])
    @app_commands.choices(ability=[app_commands.Choice(name=discipline, value=discipline) for discipline in discipline_choices])
    async def challenge(self, interaction: discord.Interaction, player: discord.Member, attribute: str, ability: str,
                        discipline: str, difficulty: int, action: str, hidden: bool = True):
        aggressor_dicepool = await handle_challenge(interaction, attribute, ability, discipline)

