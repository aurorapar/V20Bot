from typing import Optional

import discord

from ...helpers.dice_functions import rolld10


async def handle_roll(interaction: discord.Interaction, difficulty: int, dice_pool: int, auto_successes: Optional[int] = 0,
              specialized: Optional[bool] = False, willpower_used: Optional[bool] = False):

    mention_string = interaction.user.mention

    if difficulty not in range(1,11):
        return await interaction.response.send_message(f"{mention_string} The difficulty must be between 1 and 10")

    if dice_pool < 1:
        return await interaction.response.send_message(f"{mention_string} The dice pool must have at least 1 die")


    response = (f'{mention_string} started a challenge:'
                          f'\n\tDifficulty: {difficulty}'
                          f'\n\tDice Pool: {dice_pool}'
                          f'\n\tAuto Successes: {auto_successes}'
                          f'\n\tWillpower Used: {"Yes" if willpower_used else "No"}'
                          f'\n\tSpecialty: {"Yes" if specialized else "No"}\n')

    results = [difficulty for success in range(auto_successes)] + [rolld10() for die in range(dice_pool)]
    results.sort()
    explosions = 0
    if specialized:
        explosions = len([result for result in results if result == 10])
    failures = len([result for result in results if result == 1])
    successes = len([result for result in results if result >= difficulty])

    successes_after_failures = successes - failures + explosions

    results = [str(x) for x in results]

    if failures and failures > (successes + explosions) and not willpower_used:
        response += f'You botched the roll!\nRolls: ' + ' '.join(results)
        await interaction.response.send_message(response)
        return

    if successes_after_failures < 1 and willpower_used:
        response += f'You rolled only 1 success using Willpower\nRolls: ' + ' '.join(results)
        await interaction.response.send_message(response)
        return

    elif successes_after_failures > 0:
        successes_after_failures += 1 if willpower_used else 0
        response += f'You rolled {successes_after_failures} total successes!\n'
        if specialized:
            response += f'You had {explosions} additional successes due to a specialty.\n'
        response += f'Rolls: ' + ' '.join(results)
        await interaction.response.send_message(response)
        return

    elif successes_after_failures < 1 and failures < 1:
        response += f'You had no successes!\nRolls: ' + ' '.join(results)
        await interaction.response.send_message(response)
        return


async def set_bot_channel(member: discord.Member, interaction: discord.Interaction, channel: discord.TextChannel):

    user = interaction.user
    if not user.guild_permissions.manage_roles:
        return

    guild = interaction.guild

    for guild_channel in guild.channels:
        if guild_channel.id != channel.id:

            overwrite = discord.PermissionOverwrite()
            overwrite.send_messages = False
            overwrite.use_application_commands = False
            guild_channel.set_permissions(member, overwrite=overwrite)

        else:
            overwrite = discord.PermissionOverwrite()
            overwrite.send_messages = True
            overwrite.use_application_commands = True
            guild_channel.set_permissions(member, overwrite=overwrite)
            await guild_channel.send(f"I have been set to this channel by {interaction.user.mention}")


