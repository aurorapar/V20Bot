import discord

from ..user_data_objects import UserData, UserDataKeys
from ..character.attribute import Attribute
from ..character.ability import Ability
from ..character.discipline import Discipline


class CharacterEmbed(discord.Embed):
    def __init__(self, user: discord.Member, color: bytes = 0x700000):
        user_data = UserData(user.id)
        sheet_details = user_data.UserData
        sheet_details["Name"] = sheet_details["Name"] if "Name" in sheet_details.keys() else user.display_name
        super(CharacterEmbed, self).__init__(title=sheet_details["Name"], description="", color=color)

        character_image = user_data.get_data_value(UserDataKeys.THUMBNAIL_LINK)
        self.set_author(name=user.display_name, icon_url=user.avatar.url)
        self.set_thumbnail(url=character_image)

        attributes = [f"{attribute} {sheet_details[attribute]}" for attribute in Attribute]
        self.add_field(name="Attributes", value="\n".join(attributes), inline=True)

        abilities = [f"{ability} {sheet_details[ability]}" for ability in Ability if sheet_details[ability] > 0]
        self.add_field(name="Abilities", value="\n".join(abilities), inline=True)

        disciplines = [f"{discipline} {sheet_details[discipline]}" for discipline in Discipline if discipline in sheet_details.keys() and sheet_details[discipline] > 0]
        self.add_field(name="Disciplines", value="\n".join(disciplines), inline=True)

    def add_newline(self):
        self.add_field(name="\u200B", value="\u200B")


