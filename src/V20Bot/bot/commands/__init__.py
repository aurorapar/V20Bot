from discord.ext.commands import Bot

from .challenge import Challenge
from .roll import Roll
from .setcharacterimage import SetCharacterImage
from .importsheet import ImportSheet
from .character import Character


async def initialize_commands(bot: Bot):
    for command in [Challenge, Roll, SetCharacterImage, ImportSheet, Character]:
        await bot.add_cog(command(Bot))
        print(f"{command.__name__} registered!")
