import random

import discord
from discord.ext import commands, tasks
from utilites import unix_to_time, make_tiny

client = commands.Bot(command_prefix="s!")
client.remove_command("help")
statuses = ["Trading skins", "Buying skins", "Making a loudout"]
commands = [["price", "<weapon>  <skin> | Note, both parameters can be specified as 'random'"]]
last_skin_embed = discord.Embed()


@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.playing, name=random.choice(statuses)))


def help_embed():
    total = len(commands)
    embed = discord.Embed(title="Commands List", description=f"{total} Total\n", color=0xff0000)
    embed.set_author(name="CS Skin Bot",icon_url="https://www.nicepng.com/png/detail/346-3461600_csgo-case-cs-go-icon.png")
    embed.set_thumbnail(url="https://www.freepngimg.com/thumb/orange/89751-silhouette-kliktech-global-offensive-source-counterstrike-sky.png")
    for command in commands:
        embed.add_field(name=command[0], value=command[1], inline=True)
    embed.set_footer(text="Thank you for using CS Skin Bot! Devloped by Nman4#6604 https://github.com/NMan1")
    return embed


def skin_embed(weapon, skin, quality, color, skin_img, withdrable_text, data, cheapest_listing, discount):
    embed = discord.Embed(title=f"{weapon} | {skin} {quality}", description="s!add to add to virtual inventory",
                          colour=color)
    embed.set_thumbnail(url=skin_img)
    embed.add_field(name="Withdrawable In", value=withdrable_text, inline=False)
    embed.add_field(name="Updated At", value=f"{unix_to_time(data['updated_at'])}", inline=True)
    embed.add_field(name="Wear", value=cheapest_listing['float_value'], inline=True)
    embed.add_field(name=chr(173), value=chr(173))
    embed.add_field(name="Lowest Price", value=f"${data['lowest_price']} {discount}", inline=True)
    embed.add_field(name="Highest Price", value=f"${data['highest_price']}", inline=True)
    embed.add_field(name=chr(173), value=chr(173))
    embed.add_field(name="Inspect In Game", value=f"[Click Here]({make_tiny(cheapest_listing['inspect_link'])})", inline=True)
    embed.add_field(name="Buy On BitSkins", value=f"[Click Here](https://bitskins.com/view_item?app_id=730&item_id={cheapest_listing['item_id']})", inline=True)
    return embed
