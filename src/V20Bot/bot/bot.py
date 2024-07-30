import traceback
from typing import Optional, Any

import discord
from discord import app_commands

from .event_handlers import message, commands
from ..settings.settings import GUILD_IDS

MY_GUILDS = [discord.Object(id=GUILD_ID) for GUILD_ID in GUILD_IDS]


class DiscordBot(discord.Client):

    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    def on_error(self, event_method: str, /, *args: Any, **kwargs: Any) -> None:
        print('An error occurred!')
        print(traceback.format_exc())

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        for guild in MY_GUILDS:
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)

    async def on_message(self, discord_message):
        message.handle_message(discord_message)

    async def on_guild_join(self, guild):
        print('Joined guild')
        await message.send_message(self, 'Testing join message')


intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
discord_bot = DiscordBot(intents=intents)


@discord_bot.tree.command()
@app_commands.describe(
    difficulty='The difficulty of the role (set by ST)',
    dicepool='The total number of dice you have in your dice pool, including auto-successes',
    autosuccesses='The number of auto-successes (due to Disciplines)',
    specialized='Whether you are specialized in the roll',
    willpowerused='Whether Willpower was spent on the roll'
)
async def roll(interaction: discord.Interaction, difficulty: int, dicepool: int, autosuccesses: Optional[int] = 0,
              specialized: Optional[bool] = False, willpowerused: Optional[bool] = False):
    try:
        return await commands.handle_roll(interaction, difficulty, dicepool, autosuccesses, specialized, willpowerused)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        await interaction.response.send_message('Sorry, the bot broke :\\')

