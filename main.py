import difflib
import discord
import random

from bitskins import Bitskins
from utilites import subtract_time, current_time, from_timestamp
from utilites.discord import help_embed, client, change_status
from utilites.weapon import make_weapon_choice, clean_weapon, get_skin_image, format_skins

bitskins = None
bitskins_api_key = 'e49cf7e4-f72f-43ea-986e-714ab8cec13b'
bitskins_secret = '5SSNCGMUFG3M7SXJ'


@client.command(pass_context=True)
async def help(ctx):
    await ctx.send(embed=help_embed())


@client.command(pass_context=True)
async def price(ctx, weapon, *, arg=None):
    weapon, skin, quality = make_weapon_choice(weapon, arg)
    weapon = clean_weapon(weapon)
    await ctx.send(f"{weapon} | {skin} | {quality}")

    return
    skin_img = get_skin_image(weapon, skin)

    cheapest_listing = bitskins.get_request("get_inventory_on_sale", {"market_hash_name": search_query, "max_price": data['lowest_price']})
    cheapest_listing = cheapest_listing['data']['items'][0]

    withdrawable_at = subtract_time(current_time(), from_timestamp(float(cheapest_listing['withdrawable_at'])))

    discount = int(100 * (float(cheapest_listing['suggested_price']) - float(cheapest_listing['price'])) / float(cheapest_listing['suggested_price']))

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
    global bitskins
    print("The bot is ready!")
    bitskins = Bitskins(bitskins_api_key, bitskins_secret)
    format_skins()
    change_status.start()


if __name__ == '__main__':
    client.run("NzQ4MTg5Mjc2MDAwMjIzMzI1.X0ZzkA.CZ7LGVmIiEqPneuciU0CEb0GxU8")
