import discord

def handle_message(message):
    pass

async def send_message(client: discord.Client, message):
    for channel in client.get_all_channels():
        if channel.type != discord.enums.ChannelType.text:
            continue

        member = [x for x in client.get_all_members() if x.id == client.user.id]
        if member:
            member = member[0]
        else:
            return
        permissions = channel.permissions_for(member)
        if permissions.send_messages:
            # await channel.send(content=message)
            pass
        print(channel.name)
