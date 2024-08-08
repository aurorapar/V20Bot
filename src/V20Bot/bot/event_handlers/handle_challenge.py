import asyncio

import discord

from ...character import PhysicalDiscipline, PhysicalAttribute
from ...settings import willpower_icon, dice_roll_icons
from ...views import ChallengeView


async def handle_challenge(interaction: discord.Interaction, attribute: str, ability: str, discipline: str):
    def valid_int_reply(m):
        return m.content.split(' ')[-1].strip().isdigit()

    difficulty = dicepool = autosuccesses = willpower = blood = ""

    async def respond(*args, **kwargs):
        return await interaction.response.send_message(*args, **kwargs)

    async def update_challenge(*args, **kwargs):
        await interaction.edit_original_response(*args, **kwargs)

    async def get_response(*args, **kwargs):
        try:
            return await interaction.client.wait_for("message", check=valid_int_reply)
        except asyncio.Timeout:
            await update_challenge(content=f"You didn't respond within the time limit ({kwargs['timeout']}s)")
            return None

    def get_message(addition: str = ""):
        return f"Difficulty: {difficulty}\tDice Pool: {dicepool}\nWillpower: {willpower}" +\
               f"\tAutoSuccesses: {autosuccesses}\tBlood Spent: {blood}\n\n{addition}"

    def difficulty_check(message):
        return message.content.startswith('difficulty') and message.content.split(' ')[-1].isdigit()

    pre_message = f"Select the difficulty, then click the buttons below to spend Willpower and Blood, then the checkmark once you're finished.\n\n"
    challenge_view = ChallengeView(interaction.user, attribute=attribute, ability=ability, discipline=discipline)
    try:
        await interaction.response.send_message(content=get_message(pre_message), ephemeral=True, view=challenge_view)
        challenge_view.edit_original_response = interaction.edit_original_response
        await challenge_view.edit_original_response(content=challenge_view.base_message)
    except asyncio.Timeout:
        await interaction.followup(content=f"You didn't respond within the time limit ({challenge_view.timeout}s)")

    # await update_challenge(
    #     content=get_message("Enter your dicepool\n(don't include autosuccesses)\n(Type 'autosuccesses X')"))
    #
    # dicepool_response = await get_response(event="message", check=valid_int_reply, timeout=30)
    # if not dicepool_response:
    #     return
    # dicepool_response = await get_response("message", check=valid_int_reply)
    # dicepool = int(dicepool_response.content.strip())
    # await update_challenge(content=get_message("Do you want to use Willpower?\n(yes/1/true/no/0/false)"))


