import os
import traceback

from V20Bot.settings.settings import BOT_TOKEN
from V20Bot.bot.bot import discord_bot


def main(bot_token):
    try:
        if not bot_token:
            if 'DISCORD_BOT_TOKEN' in os.environ.keys():
                bot_token = os.environ['DISCORD_BOT_TOKEN']
        if not bot_token:
            bot_token = input("Please enter your bot token: ")

        discord_bot.run(bot_token)

    except Exception as e:
        print("bot was unable to connect to server.")
        print(e)
        print(traceback.format_exc())


if __name__ == "__main__":
    main(BOT_TOKEN)
