import difflib
import random
import json
import warnings

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from utilites import has_number, contains_sub

weapons = []
qualitys = ["Factory New", "Battle-Scarred", "Well-Worn", "Field-Tested", "Minimal Wear", "Random"]
raritys = [("Consumer Grade", 0xafafaf), ("Industrial Grade", 0x6496e1), ("Mil-Spec Grade", 0x4b69cd), ("Restricted", 0x8847ff), ("Classified", 0xd32ce6), ("Covert", 0xeb4b4b)]
skin_json = None
skin_urls_json = None

weapon_names = {"Pistols": {"seven": "Five-SeveN", "tec": "Tec-9", "CZ75": "CZ75-Auto", "glock": "Glock-18", "usp": "USP-S"},
                "Shotguns": {"nova": "Nova", "mag-7": "MAG-7", "xm": "XM1014"},
                "Knives": {"bayonet": "★ M9 Bayonet", "shadow": "★ Shadow Daggers", "karambit": "★ Karambit"},
                "Heavy": {"negev": "Negev"}
                }


def format_skins():
    global skin_json, skin_urls_json
    with open("bot/skins/skins.json", encoding="utf8") as file:
        skin_json = json.load(file)

    with open("bot/skins/skins_urls.json", encoding="utf8") as file:
        skin_urls_json = json.load(file)

    for weapon in skin_json:
        weapons.append(weapon)


def get_skin_image(weapon, skin):
    return skin_urls_json[weapon][skin]


def clean_weapon(weapon):
    if len(weapon.split()) > 1:
        if has_number(weapon):
            weapon = weapon.upper()
        else:
            weapon = weapon.title()
    elif has_number(weapon):
        if contains_sub(weapon, "-"):
            weapon = weapon.upper()
        else:
            weapon = weapon.upper()
    else:
        if contains_sub(weapon, "-"):
            weapon = weapon.replace("-", " ")
            weapon = weapon.title()
            weapon = weapon.replace(" ", "-")
        else:
            weapon = weapon.upper()

    for weapon_type in weapon_names:
        for find_name in weapon_names[weapon_type]:
            if contains_sub(weapon, find_name):
                weapon = weapon_names[weapon_type][find_name]

    if contains_sub(weapon, "knife"):
        weapon = "★ " + weapon

    return weapon


def make_weapon_choice(weapon, args):
    if weapon.lower() == "random":
        weapon = random.choice(weapons)
    else:
        weapon = difflib.get_close_matches(weapon.upper(), weapons, cutoff=.1)[0]

    skin_key = []
    for skin in skin_json[weapon]:
        skin_key.append(skin)

    skin_key.append("Random")
    split = args.rsplit(" ")

    skin = ["", 0]
    for word in split:
        extracted_skin = process.extract(split[0], skin_key, limit=2)
        if extracted_skin[0][1] > skin[1]:
            skin = extracted_skin[0]
            split.remove(word)

    for word in split:
        if contains_sub(skin[0], word) and not contains_sub(skin[0], "random"):
            split.remove(word)

    quality = ["", 0]
    for word in split:
        extracted_quality = process.extract(split[0], qualitys, limit=2)
        if extracted_quality[0][1] > quality[1]:
            quality = extracted_quality[0]
            split.remove(word)

    if quality[1] == 0:
        quality = [qualitys[0], 100]
    elif quality[0] == "Random":
        quality = [random.choice(qualitys[0:len(qualitys)-1]), 100]

    if skin[0] == "Random":
        skin = [random.choice(skin_key[0:len(skin_key)-1]), 100]

    return weapon, skin[0], quality[0]


async def get_price_data(bitskins, ctx, search_query):
    request = bitskins.get_request("get_price_data_for_items_on_sale", {"names": search_query})
    data = request['data']['items'][0]
    if data['total_items'] == 0:
        await ctx.send(f"""```css\n[Failed to find skin for "{search_query}". Likely there is no item listing for this quality.```""")
        return None
    return data
