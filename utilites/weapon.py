import difflib
import random
import json

from utilites import has_number, contains_sub

weapons = []
qualitys = ["Factory New", "Battle-Scarred", "Well-Worn", "Field-Tested", "Minimal Wear"]
skin_json = None
skin_urls_json = None

weapon_names = {"Pistols": {"seven": "Five-SeveN", "tec": "Tec-9", "CZ75": "CZ75-Auto", "glock": "Glock-18"},
                "Shotguns": {"nova": "Nova", "mag-7": "MAG-7", "xm": "XM1014"},
                "Knives": {"bayonet": "★ M9 Bayonet", "shadow": "★ Shadow Daggers", "karambit": "★ Karambit"},
                "Heavy": {"negev": "Negev"}
                }


def format_skins():
    global skin_json, skin_urls_json
    with open("skins.json", encoding="utf8") as file:
        skin_json = json.load(file)

    with open("skins_urls.json", encoding="utf8") as file:
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
    #
    # if contains_sub(weapon, "knife") or contains_sub(weapon, "karambit") or contains_sub(weapon, "bayonet") or contains_sub(weapon, "shadow"):
    #     if contains_sub(weapon, "bayonent"):
    #         weapon = "M9 Bayonet"
    #     weapon = "★ " + weapon
    # else:
    #     if contains_sub(weapon, "seven"):
    #         weapon = "Five-SeveN"
    #     elif contains_sub(weapon, "negev"):
    #         weapon = "Negev"
    #     elif contains_sub(weapon, "nova"):
    #         weapon = "Nova"
    #     elif contains_sub(weapon, "tec"):
    #         weapon = "Tec-9"
    #     elif contains_sub(weapon, "CZ75"):
    #         weapon = "CZ75-Auto"
    #     elif contains_sub(weapon, "m9 bay"):
    #         weapon = "★ M9 Bayonet"
    #     elif contains_sub(weapon, "mag-7"):
    #         weapon = "MAG-7"


def make_weapon_choice(weapon, args):
    if weapon.lower() == "random":
        weapon = random.choice(weapons)
    else:
        weapon = difflib.get_close_matches(weapon.upper(), weapons, cutoff=.1)[0]

    quality = "None"
    for quality_ in qualitys:
        if contains_sub(args, quality_):
            quality = quality_
            args.replace(f" {quality_}", "")

    skin = args
    if args.lower() == "random":
        skin = random.choice(list(skin_json[weapon].keys()))
    else:
        skin = difflib.get_close_matches(skin.title(), skin_json[weapon], cutoff=.1)[0]
    return weapon, skin, quality










    # debug = False
    # if contains_sub(args, "DEBUG"):
    #     debug = True
    #     arg = args.replace("DEBUG", "")
    #
    # quality = None
    # for qual in qualitys:
    #     search_query = f"{weapon} | {skin} ({qual})"
    #     if debug:
    #         await ctx.send(f"Search query {search_query}")
    #
    #     request = bitskins.get_request("get_price_data_for_items_on_sale", {"names": search_query})
    #     data = request['data']['items'][0]
    #     if data['total_items'] == 0:
    #         await ctx.send(f"""```css\n[Failed to find skin for "{search_query}". Switching quality...]```""")
    #         continue
    #     else:
    #         quality = qual
    #         break
    #
    # if quality is None:
    #     await ctx.send(f"""```css\n[Failed to find skin for each quality". Likely there are no listings for this item on BitSkins.```""")
    #     return
    #
