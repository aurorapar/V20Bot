from typing import List

import discord

def handle_message(message):
    pass

async def send_message(member: discord.Member, message):

    for channel in member.guild.channels:
        if channel.type != discord.enums.ChannelType.text:
            continue

        permissions = channel.permissions_for(member)
        if permissions.send_messages:
            # await channel.send(content=message)
            pass
