from typing import Optional

import discord

from ...dtos import ResultDetails
from ...helpers.__init__ import number_to_emoji
from ...messages import SuccessFrame


async def handle_roll(interaction: discord.Interaction, dice_pool: int, difficulty: int,
                      auto_successes: Optional[int] = 0, specialized: Optional[bool] = False,
                      willpower_used: Optional[bool] = False, target: Optional[discord.Member] = None):

    if dice_pool < 1:
        await interaction.response.send_message(ephemeral=True, content='Your dice pool can\'t be negative')
        return

    if auto_successes < 0:
        await interaction.response.send_message(ephemeral=True,
                                                content='Your number of auto-successes can\'t be negative')
        return

    if difficulty not in range(1, 11):
        await interaction.response.send_message(ephemeral=True, content='The difficulty must be between 1 and 10')
        return

    result_status = ResultDetails(
        player=interaction.user.guild.get_member(interaction.user.id),
        DicePool=dice_pool,
        Difficulty=difficulty,
        Specialized=specialized,
        Willpower=willpower_used,
        AutoSuccesses=auto_successes,
        Target=target
    )
    result_status.calculate_results()

    result_message = SuccessFrame(challenge_result=result_status)

    result_icons = [number_to_emoji(result) for result in result_status.Rolls if result <= 10]
    result_icons += [number_to_emoji(int(digit)) for result in result_status.Rolls if result > 10 for digit in
                     str(result)]
    result_icons = "".join(result_icons)

    await interaction.response.send_message(content=result_icons, embed=result_message)
