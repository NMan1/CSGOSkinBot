from utilites.bitskins import Bitskins
from utilites import subtract_time, current_time, from_timestamp, unix_to_time, make_tiny
from bot.discord import help_embed, client, change_status, skin_embed
from utilites.weapon import make_weapon_choice, clean_weapon, format_skins, get_price_data, raritys


bitskins = None
bitskins_api_key = 'f,ffefefef'
bitskins_secret = 'wkdwfwkfhwf'


@client.command(pass_context=True)
async def help(ctx):
    await ctx.send(embed=help_embed())


@client.command(pass_context=True)
async def inv(ctx):
    pass


@client.command(pass_context=True)
async def track(ctx, weapon, *, arg=None):
    weapon, skin, quality = make_weapon_choice(weapon, arg)
    weapon = clean_weapon(weapon)
    track_query = f"{weapon} | {skin} ({quality})"
    await ctx.send(f"Now tracking {track_query} | Added to your inventory. (!inv)")


@client.command(pass_context=True)
async def deal(ctx):
    market = bitskins.get_request("get_price_data_for_items_on_sale", {"app_id": 730})['data']['items']
    most_discounted_item = None
    last_discount = 0

    for item in market:
        try:
            discount = int(
                100 * (float(item['recent_sales_info']['average_price']) - float(item['lowest_price'])) / float(
                    item['recent_sales_info']['average_price']))
            if discount > last_discount:
                cheapest_listing = bitskins.get_request("get_inventory_on_sale", {"market_hash_name": most_discounted_item['market_hash_name'], "max_price": most_discounted_item['lowest_price']})
                cheapest_listing = cheapest_listing['data']['items'][0]
                if cheapest_listing:
                    last_discount = discount
                    most_discounted_item = item
                    print(discount)
        except Exception:
            pass

    print(cheapest_listing)
    cheapest_listing = cheapest_listing['data']['items'][0]
    skin_img = cheapest_listing['image']

    withdrawable_at = subtract_time(current_time(), from_timestamp(float(cheapest_listing['withdrawable_at'])))
    discount = int(100 * (float(cheapest_listing['suggested_price']) - float(cheapest_listing['price'])) / float(cheapest_listing['suggested_price']))

    discount = f"(%{discount} Off)" if 0 < discount <= 100 else ""

    if withdrawable_at.days >= 0:
        time = f"{withdrawable_at.days} Days, {withdrawable_at.seconds // 3600} hours"
    else:
        time = f"{withdrawable_at.days} Day, {withdrawable_at.seconds // 3600} hours"

    if withdrawable_at.days > 1:
        withdrable_text = f"""```css\n[{time}]```"""
    elif 1 >= withdrawable_at.days >= 0:
        withdrable_text = f"""```css\n{time}```"""
    else:
        withdrable_text = f"""```css\nInstantly Withdrawable!```"""

    color = 0xcaab05
    for rarity in raritys:
        if rarity[0] == cheapest_listing['tags']['rarity']:
            color = rarity[1]

    embed = skin_embed(weapon, skin, quality, color, skin_img, withdrable_text, data, cheapest_listing, discount)

    if data['recent_sales_info']:
        embed.add_field(name=f"Average Price (over {int(float(data['recent_sales_info']['hours']))} hours)", value=f"${data['recent_sales_info']['average_price']}", inline=False)
    else:
        embed.add_field(name=f"Average Price", value=f"Failed to find average price - no recent sales", inline=False)
    await ctx.send(embed=embed)



@client.command(pass_context=True)
async def price(ctx, weapon, *, arg=None):
    weapon, skin, quality = make_weapon_choice(weapon, arg)
    weapon = clean_weapon(weapon)

    search_query = f"{weapon} | {skin} ({quality})"
    data = await get_price_data(bitskins, ctx, search_query)
    if data is None:
        return

    cheapest_listing = bitskins.get_request("get_inventory_on_sale", {"market_hash_name": search_query, "max_price": data['lowest_price']})
    cheapest_listing = cheapest_listing['data']['items'][0]
    skin_img = cheapest_listing['image']

    withdrawable_at = subtract_time(current_time(), from_timestamp(float(cheapest_listing['withdrawable_at'])))
    discount = int(100 * (float(cheapest_listing['suggested_price']) - float(cheapest_listing['price'])) / float(cheapest_listing['suggested_price']))

    discount = f"(%{discount} Off)" if 0 < discount <= 100 else ""

    if withdrawable_at.days >= 0:
        time = f"{withdrawable_at.days} Days, {withdrawable_at.seconds // 3600} hours"
    else:
        time = f"{withdrawable_at.days} Day, {withdrawable_at.seconds // 3600} hours"

    if withdrawable_at.days > 1:
        withdrable_text = f"""```css\n[{time}]```"""
    elif 1 >= withdrawable_at.days >= 0:
        withdrable_text = f"""```css\n{time}```"""
    else:
        withdrable_text = f"""```css\nInstantly Withdrawable!```"""

    color = 0xcaab05
    for rarity in raritys:
        if rarity[0] == cheapest_listing['tags']['rarity']:
            color = rarity[1]

    embed = skin_embed(weapon, skin, quality, color, skin_img, withdrable_text, data, cheapest_listing, discount)

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
