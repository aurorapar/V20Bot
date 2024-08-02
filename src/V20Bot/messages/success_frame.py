import discord

from ..dtos import ResultDetails
from ..user_data_objects import UserData
from ..user_data_objects import UserDataKeys


class SuccessFrame(discord.Embed):

    def __init__(self, challenge_result: ResultDetails, color: bytes = 0x700000):
        title = f"{challenge_result.Player.display_name}'s Challenge" \
                if not challenge_result.Target else \
                f"{challenge_result.Player.display_name} Challenged {challenge_result.Target.display_name}"
        super(SuccessFrame, self).__init__(title=title, description="", color=color)
        self.__set_fields(challenge_result)

    def set_values(self, **kwargs):
        self.__dict__.update(kwargs)

    def __set_fields(self, challenge_result: ResultDetails):
        user_data = UserData(challenge_result.Player.id)
        self.set_thumbnail(url=user_data.get_data_value(UserDataKeys.THUMBNAIL_LINK))
        self.set_author(name=challenge_result.Player.display_name, icon_url=challenge_result.Player.avatar.url)
        self.add_field(name=challenge_result.Result, value=challenge_result.ResultMessage, inline=False)
        self.add_field(name="Difficulty", value=challenge_result.Difficulty, inline=True)
        self.add_field(name="Dice Pool", value=challenge_result.DicePool, inline=True)
        self.__add_newline()
        self.add_field(name="Willpower", value=f"Not Used" if not challenge_result.Willpower else "Used", inline=True)
        self.add_field(name="Auto Successes",
                       value=f"None" if not challenge_result.AutoSuccesses else challenge_result.AutoSuccesses, inline=True)
        self.add_field(name="Specialized", value=f"No" if not challenge_result.Specialized else "Yes", inline=True)

    def __add_newline(self):
        self.add_field(name="\u200B", value="\u200B")


