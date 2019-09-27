import discord
from discord.ext import commands
import asyncio
import time

client = commands.Bot(command_prefix="!", case_insensitive=False)
client.remove_command("help")

"""
-------------
This tutorial is different from the others in numerous ways.
I'll be going over basic converters and arguments.
As always, please refer to the discord.py documentation. Link is in the README.
-------------
"""

@client.event
async def on_ready():
    print("I'm online!")
    
@client.command()
async def warn(ctx, member: discord.Member=None, *, reason: str):
    if not member:
        await ctx.send("You didn't specify a member!")
    else:
        await ctx.send("**{}** has been warned for `{}`!".format(member.name, reason))
        
client.run("token")
        
