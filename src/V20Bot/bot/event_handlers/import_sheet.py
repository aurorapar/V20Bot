import urllib.request

import discord
from pypdf import PdfReader, errors

from ...messages.character_frame import CharacterFrame
from ...PdfExtractor import retrieve_sheet_details
from ...user_data_objects import UserData

TEMP_SHEET_FILE = "temp_character.pdf"


async def import_sheet(interaction: discord.Interaction, link):
    user_data = UserData(interaction.user.id)
    link_verified, user_response = verify_link(link)
    if not link_verified:
        await interaction.response.send_message(ephemeral=True, content=user_response)
        return

    user_data.set_character_sheet(retrieve_sheet_details(TEMP_SHEET_FILE))
    example = CharacterFrame(interaction.user)
    await interaction.response.send_message(ephemeral=True,
                                            content="You have updated your sheet!", embed=example)


def verify_link(link):
    try:
        response = urllib.request.urlopen(link)
        if response.status not in [200]:
            error_message = "You didn't provide a valid link. Site down?"
            return False, error_message
        try:
            urllib.request.urlretrieve(link, TEMP_SHEET_FILE)
            sheet = PdfReader(TEMP_SHEET_FILE)
        except errors.PdfStreamError:
            error_message = "You didn't provide a valid Pdf. Use Mr. Gones Interactive Neonate Sheets"
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