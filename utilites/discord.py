import random

import discord
from discord.ext import commands, tasks

client = commands.Bot(command_prefix="s!")
client.remove_command("help")
statuses = ["Trading skins", "Buying skins", "Making a loudout"]
commands = [["price", "<weapon>  <skin> | Note, both paramters can be specified as 'random'"]]


@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=random.choice(statuses)))


def help_embed():
    total = len(commands)
    embed = discord.Embed(title="Commands List", description=f"{total} Total\n", color=0xff0000)
    embed.set_author(name="CS Skin Bot", icon_url="https://www.nicepng.com/png/detail/346-3461600_csgo-case-cs-go-icon.png")
    embed.set_thumbnail(url="https://www.freepngimg.com/thumb/orange/89751-silhouette-kliktech-global-offensive-source-counterstrike-sky.png")
    for command in commands:
        embed.add_field(name=command[0], value=command[1], inline=True)
    embed.set_footer(text="Thank you for using CS Skin Bot! Devloped by Nman4#6604 https://github.com/NMan1")
    return embed

