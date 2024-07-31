roll_icons = {
    '0': "0️⃣",
    '1': "1️⃣",
    '2': "2️⃣",
    '3': "3️⃣",
    '4': "4️⃣",
    '5': "5️⃣",
    '6': "6️⃣",
    '7': "7️⃣",
    '8': "8️⃣",
    '9': "9️⃣",
    '10': "🔟"
}


def number_to_emoji(number: int):
    return ''.join([roll_icons[x] for x in str(number)] if number > 10 else [roll_icons[str(number)]])
