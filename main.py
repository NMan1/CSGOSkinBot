import contextlib
import difflib
import json
import time
from urllib.parse import urlencode
from urllib.request import urlopen

import requests
import pyotp
import discord
import random
import base64
import os
import tzlocal

import datetime
from discord.ext import commands, tasks
from discord.utils import get

from bitskins import Bitskins

music = None
client = commands.Bot(command_prefix="s!")
client.remove_command("help")
list_of_status = ["Trading skins", "Buying skins", "Making a loudout"]
list_of_commands = [["price", "<weapon>  <skin> | Note, both paramters can be specified as 'random'"]]

bs = None
bitskins_api_key = 'e49cf7e4-f72f-43ea-986e-714ab8cec13b'
bitskins_secret = '5SSNCGMUFG3M7SXJ'

skin_json = None
skin_urls_json = None
weapon_list = []
qualitys = ["Factory New", "Battle-Scarred", "Well-Worn", "Field-Tested", "Minimal Wear"]


def make_tiny(url):
    request_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url': url}))
    with contextlib.closing(urlopen(request_url)) as response:
        return response.read().decode('utf-8 ')


@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.playing, name=list_of_status[random.randint(0, 2)]))


def embed_help(list_of_list):
    total = len(list_of_list)
    embed = discord.Embed(title="Commands List", description=f"{total} Total\n", color=0xff0000)
    embed.set_author(name="CS Skin Bot", icon_url="https://www.nicepng.com/png/detail/346-3461600_csgo-case-cs-go-icon.png")
    embed.set_thumbnail(url="https://www.freepngimg.com/thumb/orange/89751-silhouette-kliktech-global-offensive-source-counterstrike-sky.png")
    for list in list_of_list:
        embed.add_field(name=list[0], value=list[1], inline=True)
    embed.set_footer(text="Thank you for using CS Skin Bot! Devloped by Nman4#6604 https://github.com/NMan1")
    return embed


@client.command(pass_context=True)
async def help(ctx):
    await ctx.send(embed=embed_help(list_of_commands))


@client.command(pass_context=True)
async def price(ctx, weapon, *, arg=None):
    given_weapon = weapon
    if weapon.lower() == "random":
        weapon = random.choice(weapon_list)
    else:
        weapon = difflib.get_close_matches(weapon.upper(), weapon_list, cutoff=.1)[0]

    debug = False
    if arg.find("DEBUG") != -1:
        debug = True
        arg = arg.replace("DEBUG", "")

    given_skin = arg
    if arg.lower() == "random":
        skin = random.choice(list(skin_json[weapon].keys()))
    else:
        skin = difflib.get_close_matches(given_skin.title(), skin_json[weapon], cutoff=.1)[0]

    skin_img = skin_urls_json[weapon][skin]
    if weapon.lower().find("knife") != -1 or weapon.lower().find("karambit") != -1 or weapon.lower().find("bayonet") != -1 or weapon.lower().find("shadow") != -1:
        weapon = "★ " + weapon
    elif weapon.lower().find("mag-7") != -1:
        weapon = "MAG-7"

    def has_number(string):
        return any(char.isdigit() for char in string)

    if len(weapon.split()) > 1:
        if has_number(weapon):
            weapon = weapon.upper()
        else:
            weapon = weapon.title()
    elif has_number(weapon):
        if weapon.find("-") != -1:
            if weapon.lower().find("glock") != -1:
                weapon = "Glock-18"
            else:
                weapon = weapon.upper()
        else:
            weapon = weapon.upper()
    else:
        if weapon.find("-") != -1:
            weapon = weapon.replace("-", " ")
            weapon = weapon.title()
            weapon = weapon.replace(" ", "-")
        else:
            weapon = weapon.upper()

    if weapon.lower().find("seven") != -1:
        weapon = "Five-SeveN"
    elif weapon.lower().find("negev") != -1:
        weapon = "Negev"
    elif weapon.lower().find("nova") != -1:
        weapon = "Nova"
    elif weapon.lower().find("tec") != -1:
        weapon = "Tec-9"
    elif weapon.lower().find("CZ75") != -1:
        weapon = "CZ75-Auto"
    elif weapon.lower().find("m9 bay") != -1:
        weapon = "★ M9 Bayonet"


    quality = None
    for qual in qualitys:
        search_query = f"{weapon} | {skin} ({qual})"
        if debug:
            await ctx.send(f"Search query {search_query}")

        request = bs.get_request("get_price_data_for_items_on_sale", {"names": search_query})
        data = request['data']['items'][0]
        if data['total_items'] == 0:
            await ctx.send(f"""```css\n[Failed to find skin for "{search_query}". Switching quality...]```""")
            continue
        else:
            quality = qual
            break

    if quality is None:
        await ctx.send(f"""```css\n[Failed to find skin for each quality". Likely there are no listings for this item on BitSkins.```""")
        return

    def unix_to_time(unix):
        unix_timestamp = float(unix)
        local_timezone = tzlocal.get_localzone()  # get pytz timezone
        local_time = datetime.datetime.fromtimestamp(unix_timestamp, local_timezone)
        if local_time.hour < 12:
            if local_time.hour < 10:
                return str(local_time)[len("2020-06-18") + 2:len(str(local_time)) - 6] + " AM"
            else:
                return str(local_time)[len("2020-06-18") + 2:len(str(local_time)) - 6] + " AM"
        miliTime = str(local_time)[len("2020-06-18") + 1:len(str(local_time)) - 6]
        miliTime = miliTime[:-3]
        hours, minutes = miliTime.split(":")
        hours, minutes = int(hours), int(minutes)
        setting = "AM"
        if hours > 12:
            setting = "PM"
            hours -= 12
        return f"{hours}:{minutes} " + setting

    cheapest_listing = bs.get_request("get_inventory_on_sale",
                                      {"market_hash_name": search_query, "max_price": data['lowest_price']})
    cheapest_listing = cheapest_listing['data']['items'][0]

    a = datetime.datetime.now()
    unix_timestamp = float(cheapest_listing['withdrawable_at'])
    local_timezone = tzlocal.get_localzone()  # get pytz timezone
    local_time = datetime.datetime.fromtimestamp(unix_timestamp, local_timezone)
    local_time = local_time.replace(tzinfo=None)
    withdrawable_at = local_time - a

    discount = int(100 * (float(cheapest_listing['suggested_price']) - float(cheapest_listing['price'])) / float(
        cheapest_listing['suggested_price']))

    if 0 < discount <= 100:
        discount_text = f"(%{discount} Off)"
    else:
        discount_text = ""

    if withdrawable_at.days > 1:
        time = f"{withdrawable_at.days} Days, {withdrawable_at.seconds // 3600} hours"
    elif withdrawable_at.days == 0:
        time = f"{withdrawable_at.days} Days, {withdrawable_at.seconds // 3600} hours"
    else:
        time = f"{withdrawable_at.days} Day, {withdrawable_at.seconds // 3600} hours"

    if withdrawable_at.days > 1:
        withdrable_text = f"""```css\n[{time}]```"""
    elif 1 >= withdrawable_at.days >= 0:
        withdrable_text = f"""```css\n{time}```"""
    else:
        withdrable_text = f"""```css\nInstantly Withdrawable!```"""


    embed = discord.Embed(title=f"{weapon} | {skin} {quality}", colour=0xcaab05)
    embed.set_thumbnail(url=skin_img)
    embed.add_field(name="Withdrawable In", value=withdrable_text, inline=False)
    embed.add_field(name="Updated At", value=f"{unix_to_time(data['updated_at'])}", inline=True)
    embed.add_field(name="Wear", value=cheapest_listing['float_value'], inline=True)
    embed.add_field(name=chr(173), value=chr(173))
    embed.add_field(name="Lowest Price", value=f"${data['lowest_price']} {discount_text}", inline=True)
    embed.add_field(name="Highest Price", value=f"${data['highest_price']}", inline=True)
    embed.add_field(name=chr(173), value=chr(173))
    embed.add_field(name="Inspect In Game", value=f"[Click Here]({make_tiny(cheapest_listing['inspect_link'])})",
                    inline=True)
    embed.add_field(name="Buy On BitSkins",
                    value=f"[Click Here](https://bitskins.com/view_item?app_id=730&item_id={cheapest_listing['item_id']})",
                    inline=True)

    if data['recent_sales_info']:
        embed.add_field(name=f"Average Price (over {int(float(data['recent_sales_info']['hours']))} hours)", value=f"${data['recent_sales_info']['average_price']}", inline=False)
    else:
        embed.add_field(name=f"Average Price", value=f"Failed to find average price - no recent sales", inline=False)
    await ctx.send(embed=embed)



@client.event
async def on_ready():
    print("The bot is ready!")
    change_status.start()


def format_skins():
    global skin_json, skin_urls_json
    with open("skins.json", encoding="utf8") as file:
        skin_json = json.load(file)

    with open("skins_urls.json", encoding="utf8") as file:
        skin_urls_json = json.load(file)

    for weapon in skin_json:
        weapon_list.append(weapon)


if __name__ == '__main__':
    bs = Bitskins(bitskins_api_key, bitskins_secret)
    format_skins()
    client.run("NzQ4MTg5Mjc2MDAwMjIzMzI1.X0ZzkA.CZ7LGVmIiEqPneuciU0CEb0GxU8")
