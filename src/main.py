import asyncio
import os
import traceback

from V20Bot.settings import TESTING
from V20Bot.bot import discord_bot
from V20Bot.bot import initialize_commands


def main():
    try:
        bot_token = os.environ['DISCORD_BOT_TOKEN'] if not TESTING else os.environ['DISCORD_TEST_TOKEN']
        asyncio.run(initialize_commands(discord_bot))
        discord_bot.run(bot_token)
    except Exception as e:
        print("bot was unable to connect to server.")
        print(e)
        print(traceback.format_exc())


if __name__ == "__main__":
    main()

