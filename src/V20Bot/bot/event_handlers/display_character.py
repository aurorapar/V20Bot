import discord

from ...messages.character_frame import CharacterFrame
from ...user_data_objects import UserData


async def display_character(interaction: discord.Interaction):
    user_data = UserData(interaction.user.id)
    if "Name" not in user_data.UserData.keys():
        await interaction.response.send_message(ephemeral=True,
                                                content="You haven't uploaded your sheet yet. Use /importsheet")
    else:
        character = CharacterFrame(interaction.user)
        await interaction.response.send_message(ephemeral=True, embed=character)
