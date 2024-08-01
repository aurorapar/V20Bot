roll_icons = {
    '0': "Are you cheating? Theres no way you have 20+ in your pool",
    '1': "<:silver1:1268448911027339307>",
    '2': "<:silver2:1268448912738488360>",
    '3': "<:silver3:1268448913556242503>",
    '4': "<:silver4:1268448914202165352>",
    '5': "<:silver5:1268448915485622343>",
    '6': "<:silver6:1268448916014239829>",
    '7': "<:silver7:1268448917297696819>",
    '8': "<:silver8:1268448949082001440>",
    '9': "<:silver9:1268448919612952609>",
    '10': "<:silver10:1268448950206201987>"
}


def number_to_emoji(number: int):
    return ''.join([roll_icons[x] for x in str(number)] if number > 10 else [roll_icons[str(number)]])
