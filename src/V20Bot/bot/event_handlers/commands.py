from typing import Optional

import discord

from ...helpers.dice_functions import rolld10
from ...helpers.helpers import number_to_emoji


async def handle_roll(client: discord.Client, interaction: discord.Interaction, dice_pool: int, difficulty: int,
                      auto_successes: Optional[int] = 0, specialized: Optional[bool] = False,
                      willpower_used: Optional[bool] = False, target: Optional[discord.Member] = None):

    name = interaction.user.display_name

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

    results = [difficulty for _ in range(auto_successes)] + [rolld10() for _ in range(max(0, dice_pool - auto_successes))]
    results.sort()

    mention_string = interaction.user.mention

    willpower_message = '' if not willpower_used else f'spent Willpower'
    autosuccess_message = '' if not auto_successes else f'has {number_to_emoji(auto_successes)} Autosuccesses'
    specialized_message = '' if not specialized else f'has specialized!'
    extra_messages = [willpower_message, autosuccess_message, specialized_message]
    extra_messages = [x for x in extra_messages if x]
    if len(extra_messages):
        if len(extra_messages) > 1:
            extra_messages = f'\t\t({name} {", ".join(extra_messages[0:-1])} and {extra_messages[-1]})\n'
        else:
            extra_messages = f'\t\t({name} {''.join(extra_messages)})\n'

    response = f'{mention_string} wants to challenge {target.mention}!' if target else \
        f'{mention_string} has started a challenge!'

    response += f'\n\t{name}\'s Dice Pool:  {number_to_emoji(dice_pool)}   Difficulty:   {number_to_emoji(difficulty)}\n'
    response += extra_messages if extra_messages else ''

    explosions = 0
    if specialized:
        explosions = len([result for result in results if result == 10])
    botches = len([result for result in results if result == 1])
    successes = len([result for result in results if result >= difficulty]) + explosions

    willpower_needed = botches > successes and willpower_used
    successes = max(int(willpower_used), successes - botches)

    results = [number_to_emoji(x) for x in results]

    if not successes and botches:
        response += f'{name} botched the roll!\nRolls: ' + ' '.join(results)
        await interaction.response.send_message(response)
        return

    if willpower_needed and successes > 0:
        response += f'{name} has {number_to_emoji(successes)} success thanks to Willpower\nRolls: ' + '  '.join(results)
        await interaction.response.send_message(response)
        return

    if successes < 1:
        response += f'{name} has no successes!\nRolls: ' + '  '.join(results)
        await interaction.response.send_message(response)
        return

    if successes > 0:
        response += f'{name} rolled {number_to_emoji(successes)} total successes!'
        if specialized:
            response += f' ({number_to_emoji(explosions)} additional successes due to a specialty)'
        response += f'\nRolls: ' + '  '.join(results)
        await interaction.response.send_message(response)
        return

    response = f'The Bot was unable to determine the results.'
    response += f'\ndice_pool {dice_pool}'
    response += f'\ndifficulty {difficulty}'
    response += f'\nauto_successes {auto_successes}'
    response += f'\nwillpower_used {willpower_used}'
    response += f'\ntarget: {"None" if not target else target.display_name}'
    response += f'\nrolls: ' + '  '.join(results)
    await interaction.response.send_message(response)


async def set_bot_channel(member: discord.Member, interaction: discord.Interaction, channel: discord.TextChannel):

    user = interaction.user
    if not user.guild_permissions.manage_roles:
        return

    if not member.guild_permissions.manage_roles:
        await interaction.response.send_message(ephemeral=True, content="The bot does not have Manage Role permission.")
        return

    # return await disable(interaction)

    guild = interaction.guild

    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = True
    overwrite.use_application_commands = True
    await channel.set_permissions(member, overwrite=overwrite)
    await channel.send(f"I have been set to this channel by {interaction.user.mention}")

    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = False
    overwrite.use_application_commands = False
    for guild_channel in guild.channels:
        if guild_channel.id != channel.id:
            await guild_channel.set_permissions(member, overwrite=overwrite)


async def disable(interaction):
    return await interaction.response.send_message(ephemeral=True, content="This command has been disabled.")
