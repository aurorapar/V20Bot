import discord

from ..user_data_objects import UserData, UserDataKeys


class ExampleFrame(discord.Embed):
    def __init__(self, user: discord.Member, color: bytes = 0x700000):
        super(ExampleFrame, self).__init__(title="Example Character Image", description="", color=color)

        character_image = UserData(user.id).get_data_value(UserDataKeys.THUMBNAIL_LINK)
        self.set_author(name=user.display_name, icon_url=user.avatar.url)
        self.set_thumbnail(url=character_image)

    def add_newline(self):
        self.add_field(name="\u200B", value="\u200B")


