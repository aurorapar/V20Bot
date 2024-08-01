import discord


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
