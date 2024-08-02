from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Bot

from ..event_handlers import handle_roll


class Roll(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(description="Challenge another player")
    @app_commands.allowed_contexts(guilds=True)
    @app_commands.describe(
        difficulty='The difficulty of the role (set by ST)',
        dicepool='The total number of dice you have in your dice pool, including auto-successes',
        autosuccesses='The number of auto-successes (due to Disciplines or Blood expenditure, etc.)',
        specialized='Whether you are specialized in the roll',
        willpowerused='Whether Willpower was spent on the roll',
        target='A potential player you wish to have a contested roll with'
    )
    async def roll(self, interaction: discord.Interaction, difficulty: int, dicepool: int,
                   autosuccesses: Optional[int] = 0, specialized: Optional[bool] = False,
                   willpowerused: Optional[bool] = False, target: Optional[discord.Member] = None):
        return await handle_roll(interaction=interaction, difficulty=difficulty, dice_pool=dicepool,
                                 auto_successes=autosuccesses, specialized=specialized, target=target,
                                 willpower_used=willpowerused
        )