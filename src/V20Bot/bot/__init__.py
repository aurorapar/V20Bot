import sys
from typing import Any

import discord
from discord.ext.commands import Bot


from .commands import initialize_commands
from ..bot import event_handlers
from ..settings import BOT_USERNAME, TESTING, SYNC_ON_MESSAGE, RESYNC_ALLOWED


class DiscordBot(Bot):

    def __init__(self, *, command_prefix: str, intents: discord.Intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.synced = False

    async def on_error(self, event_method: str, /, *args: Any, **kwargs: Any) -> None:
        error = sys.exc_info()
        error_message = error[1]
        # trace = error[2]
        print(error_message)

    async def on_message(self, discord_message):
        master_user = int(discord_message.author.id) == 266328806011174912
        if discord_message.content.lower() == 'resync':
            if len([role for role in discord_message.author.roles if role.permissions.administrator]) or master_user:
                await discord_message.channel.delete_messages(messages=[discord_message])
                if not RESYNC_ALLOWED and not master_user:
                    await discord_message.author.send(content='Resyncing has been disabled.')
                    return
                if self.synced:
                    await discord_message.author.send(content='The bot has already synced.')
                    return
                await discord_message.author.send(content='Resyncing....')
                await self.tree.sync()
                await discord_message.author.send(content='Resynced!')
                self.synced = True
        if not self.synced and SYNC_ON_MESSAGE:
            await self.tree.sync()
            print(f"Tree synced!")
            self.synced = True

    async def on_ready(self):
        await self.user.edit(username=BOT_USERNAME)
        if TESTING:
            return
        for guild in self.guilds:
            member = await self.get_self_member(guild)
            await event_handlers.send_message(member, f'{self.user.name} has come out of torpor.')

    async def get_self_member(self, guild: discord.Guild):
        member = await guild.query_members(user_ids=[self.user.id])
        if not member:
            return None
        return member[0]


bot_intents = discord.Intents.default()
bot_intents.messages = True
bot_intents.guilds = True
bot_intents.presences = True
bot_intents.members = True
bot_intents.message_content = True
discord_bot = DiscordBot(command_prefix=".", intents=bot_intents)

