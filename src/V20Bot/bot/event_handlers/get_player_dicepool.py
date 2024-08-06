import asyncio

import discord


async def get_player_dicepool(interaction: discord.Interaction):
    def valid_int_reply(m):
        return m.content.strip().isdigit()

    difficulty = dicepool = autosuccesses = willpower = blood = ""

    async def respond(*args, **kwargs):
        await interaction.response.send_message(*args, **kwargs)

    async def update_challenge(*args, **kwargs):
        await interaction.edit_original_response(*args, **kwargs)

    async def get_response(*args, **kwargs):
        try:
            return await interaction.client.wait_for("message", check=valid_int_reply)
        except asyncio.Timeout:
            await update_challenge(content="You didn't respond within the time limit")
            return None

    def get_message(addition: str = ""):
        return f"Difficulty: {difficulty}\tDice Pool: {dicepool}\nWillpower: {willpower}" +\
               f"\tAutoSuccesses: {autosuccesses}\tBlood Spent: {blood}\n\n{addition}"

    def difficulty_check(message):
        return message.content.startswith('difficulty') and message.content.split(' ')[-1].isdigit()

    await respond(content=get_message("What is the Difficulty?\n(Type 'difficulty X')"), ephemeral=True)

    difficulty_response = await get_response(event="message", check=valid_int_reply, timeout=30)
    if not difficulty_response:
        return
    difficulty_response = await get_response("message", check=valid_int_reply)
    difficulty = int(difficulty_response.content.strip())
    await difficulty_response.delete()
    await update_challenge(
        content=get_message("Enter your dicepool\n(don't include autosuccesses)\n(Type 'autosuccesses X')"))

    dicepool_response = await get_response(event="message", check=valid_int_reply, timeout=30)
    if not dicepool_response:
        return
    dicepool_response = await get_response("message", check=valid_int_reply)
    dicepool = int(dicepool_response.content.strip())
    await update_challenge(content=get_message("Do you want to use Willpower?\n(yes/1/true/no/0/false)"))


