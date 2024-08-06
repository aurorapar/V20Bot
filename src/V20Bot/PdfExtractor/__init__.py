
from pypdf import PdfReader

from ..character.attribute import Attribute
from ..character.ability import Ability
from .mappings import pdf_value_mappings


def retrieve_sheet_details(url):
    sheet_details = {}

    reader = PdfReader(url)
    fields = reader.get_fields()

    for k, v in pdf_value_mappings.items():
        if isinstance(v, str):
            sheet_details[k] = fields[v]['/V']

    for attribute in Attribute:
        sheet_details[attribute] = 0
        keys = pdf_value_mappings[attribute]
        for key in keys:
            if '/V' not in fields[key].keys():
                continue
            sheet_details[attribute] += 1 if fields[key]['/V'] == '/Yes' else 0

    for ability in Ability:
        sheet_details[ability] = 0
        keys = pdf_value_mappings[ability]
        for key in keys:
            if '/V' not in fields[key].keys():
                continue
            sheet_details[ability] += 1 if fields[key]['/V'] == '/Yes' else 0

    for disc in pdf_value_mappings['Disciplines'].keys():
        if '/V' in fields[disc].keys():
            discipline_name = fields[disc]['/V'].strip()
            if len(discipline_name):
                sheet_details[discipline_name] = 0
                dot_labels = pdf_value_mappings['Disciplines'][disc]
                for dot in dot_labels:
                    if '/V' in fields[dot].keys():
                        sheet_details[discipline_name] += 1 if fields[dot]['/V'] == '/Yes' else 0

    return sheet_details
