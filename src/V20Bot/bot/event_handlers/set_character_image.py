import urllib
from io import BytesIO

import discord
from filetype import guess

from ...messages import ExampleFrame
from ...user_data_objects import UserData, UserDataKeys


async def set_character_image(interaction: discord.Interaction, link: str):
    user_data = UserData(interaction.user.id)
    if user_data.get_data_value(UserDataKeys.THUMBNAIL_LINK) == link:
        example = ExampleFrame(interaction.user)
        await interaction.response.send_message(ephemeral=True, embed=example,
                                                content="Your character image is already using that link")
        return

    link_verified, user_response = verify_link(link)
    if not link_verified:
        await interaction.response.send_message(ephemeral=True, content=user_response)
        return

    user_data.set_user_data(UserDataKeys.THUMBNAIL_LINK, link)
    example = ExampleFrame(interaction.user)
    await interaction.response.send_message(ephemeral=True,
                                            content="You have changed your Character image!", embed=example)


def verify_link(link):
    try:
        response = urllib.request.urlopen(link)
        if response.status not in [200]:
            error_message = "You didn't provide a valid link. Site down?"
            return False, error_message
        mime_type = guess(BytesIO(response.read())).mime
        if not mime_type.startswith('image'):
            error_message = "You didn't provide the link to an image! >:("
            return False, error_message
        return True, None
    except urllib.error.HTTPError as e:
        if ' 429:' in str(e):
            return False, f"That website doesn't let discord pull images from there. Try https://postimg.cc"
        print(e)
        return False, f"Sorry, something broke :\\ Please send this error to @auroratheorca: {e}"
    except Exception as e:
        print(e)
        return False, "Sorry, something broke :\\"
