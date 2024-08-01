import discord

from ..dtos import ResultDetails


class SuccessFrame(discord.Embed):

    def __init__(self, title: str, description: str, color: bytes = 0x700000, challenge_result: ResultDetails = None):
        super(SuccessFrame, self).__init__(title=title, description=description, color=color)
        if challenge_result:
            self.set_fields(challenge_result)

    def set_values(self, **kwargs):
        self.__dict__.update(kwargs)

    def set_fields(self, challenge_result: ResultDetails):
        self.set_author(name=challenge_result.Player.display_name, icon_url=challenge_result.Player.avatar.url)
        self.add_field(name=challenge_result.Result, value=challenge_result.ResultMessage, inline=False)
        self.add_field(name="Difficulty", value=challenge_result.Difficulty, inline=True)
        self.add_field(name="Dice Pool", value=challenge_result.DicePool, inline=True)
        self.add_newline()
        self.add_field(name="Willpower", value=f"Not Used" if not challenge_result.Willpower else "Used", inline=True)
        self.add_field(name="Auto Successes",
                       value=f"None" if not challenge_result.AutoSuccesses else challenge_result.AutoSuccesses, inline=True)
        self.add_field(name="Specialized", value=f"No" if not challenge_result.Specialized else "Yes", inline=True)

    def add_newline(self):
        self.add_field(name="\u200B", value="\u200B")


