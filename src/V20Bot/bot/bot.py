import sys
from typing import Optional, Any

import discord
from discord import app_commands

from .event_handlers import message, commands
from ..settings.settings import BOT_USERNAME, TESTING, RESYNC


class DiscordBot(discord.Client):

    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.synced = False

    async def on_error(self, event_method: str, /, *args: Any, **kwargs: Any) -> None:
        error = sys.exc_info()
        error_message = error[1]
        trace = error[2]
        print(error_message)

    async def on_message(self, discord_message):
        if discord_message.content.lower() == 'resync':
            if len([role for role in discord_message.author.roles if role.permissions.administrator]):
                await discord_message.channel.delete_messages(messages=[discord_message])
                if not RESYNC:
                    await discord_message.author.send(content='Resyncing has been disabled.')
                    return
                if self.synced:
                    await discord_message.author.send(content='The bot has already synced.')
                    return
                await discord_message.author.send(content='Resyncing....')
                await self.tree.sync()
                await discord_message.author.send(content='Resynced!')
                self.synced = True
        if not self.synced and RESYNC:
            await self.tree.sync()
            print(f"Tree synced!")
            self.synced = True

    async def on_ready(self):
        await self.user.edit(username=BOT_USERNAME)
        if TESTING:
            return
        for guild in self.guilds:
            member = await self.get_self_member(guild)
            await message.send_message(member, f'{self.user.name} has come out of torpor.')

    async def get_self_member(self, guild: discord.Guild):
        member = await guild.query_members(user_ids=[self.user.id])
        if not member:
            return None
        return member[0]


intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.presences = True
intents.members = True
intents.message_content = True
discord_bot = DiscordBot(intents=intents)


@discord_bot.tree.command()
@app_commands.allowed_contexts(guilds=True)
@app_commands.describe(
    difficulty='The difficulty of the role (set by ST)',
    dicepool='The total number of dice you have in your dice pool, including auto-successes',
    autosuccesses='The number of auto-successes (due to Disciplines)',
    specialized='Whether you are specialized in the roll',
    willpowerused='Whether Willpower was spent on the roll',
    target='A potential player you wish to have a contested roll with'
)
async def roll(
        interaction: discord.Interaction,
        difficulty: int,
        dicepool: int,
        autosuccesses: Optional[int] = 0,
        specialized: Optional[bool] = False,
        willpowerused: Optional[bool] = False,
        target: Optional[discord.Member] = None):
    return await commands.handle_roll(
        client=discord_bot,
        interaction=interaction,
        difficulty=difficulty,
        dice_pool=dicepool,
        auto_successes=autosuccesses,
        specialized=specialized,
        target=target,
        willpower_used=willpowerused
    )


@discord_bot.tree.command()
@app_commands.allowed_contexts(guilds=True)
@app_commands.checks.has_permissions(manage_roles=True)
@app_commands.describe(
    channel='The channel you want to allow the bot in'
)
async def setbotchannel(interaction: discord.Interaction, channel: discord.TextChannel):
    member = await discord_bot.get_self_member(interaction.guild)
    await commands.set_bot_channel(
        member,
        interaction,
        channel
    )

