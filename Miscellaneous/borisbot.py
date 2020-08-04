import discord
import asyncio
import time
import random
import requests

"""
Why did I have to make this...
Please help save my sanity...
"""

client = discord.Client()

@client.event
async def on_ready():
    print("cursed bot")

@client.event
async def on_message(msg):
    if "boris" in msg.content.lower():
        message_to_send = requests.get('https://bojo.maurom.dev').json()['quote']
        await msg.channel.send(message_to_send)

client.run("token")
    
