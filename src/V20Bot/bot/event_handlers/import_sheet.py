import urllib.request

import discord
from pypdf import PdfReader, errors

from ...messages.character_frame import CharacterFrame
from ...PdfExtractor import retrieve_sheet_details
from ...user_data_objects import UserData

TEMP_SHEET_FILE = "temp_character.pdf"


async def import_sheet(interaction: discord.Interaction, pdf: discord.Attachment):
    user_data = UserData(interaction.user.id)
    link_verified, response = await verify_pdf(pdf)
    if not link_verified:
        await interaction.response.send_message(ephemeral=True, content=response)
        return

    user_data.set_character_sheet(retrieve_sheet_details(TEMP_SHEET_FILE))
    example = CharacterFrame(interaction.user)
    await interaction.response.send_message(ephemeral=True,
                                            content="You have updated your sheet!", embed=example)


async def verify_pdf(pdf: discord.Attachment):
    try:
        with open(TEMP_SHEET_FILE, 'wb') as f:
            await pdf.save(f)
        sheet = PdfReader(TEMP_SHEET_FILE)
    except errors.PdfStreamError:
        error_message = "You didn't provide a valid Pdf. Use Mr. Gones Interactive Neonate Sheets"
        return False, error_message
    return True, None
