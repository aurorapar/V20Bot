import asyncio
import os
import traceback

from V20Bot.settings import BOT_TOKEN
from V20Bot.bot import discord_bot
from V20Bot.bot import initialize_commands


def main(bot_token):
    try:
        if not bot_token:
            if 'DISCORD_BOT_TOKEN' in os.environ.keys():
                bot_token = os.environ['DISCORD_BOT_TOKEN']
        if not bot_token:
            bot_token = input("Please enter your bot token: ")

        asyncio.run(initialize_commands(discord_bot))
        discord_bot.run(bot_token)

    except Exception as e:
        print("bot was unable to connect to server.")
        print(e)
        print(traceback.format_exc())


if __name__ == "__main__":
    main(BOT_TOKEN)

