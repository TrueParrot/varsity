import discord
import asyncio
import time
import random

"""
Why did I have to make this...
Please help save my sanity...
"""

client = discord.Client()
boris_quotes = ["My chances of being PM are about as good as the chances of finding Elvis on Mars, or my being reincarnated as an olive.",
                "It is possible to have a pretty good life and career being a leech and a parasite in the media world, gadding about from TV studio to TV studio, writing inconsequential pieces and having a good time. But in the end you have a great sense of personal dissatisfaction.",
                "There's an idea that London is a planet on its own: that it's starting to diverge from the rest of the solar system. We need to combat that.",
                "I want to win and I want to be in office.",
                "There is absolutely no one, apart from yourself, who can prevent you, in the middle of the night, from sneaking down to tidy up the edges of that hunk of cheese at the back of the fridge.",
                "I am supporting David Cameron purely out of cynical self-interest.",
                "It just happens I write fast and always have done.",
                "I'm a one-nation Tory.",
                "I'd like thousands of schools as good as the one I went to, Eton.",
                "My policy on cake is pro having it and pro eating it.",
                "My friends, as I have discovered myself, there are no disasters, only opportunities. And, indeed, opportunities for fresh disasters.",
                "Voting Tory will cause your wife to have bigger breasts and increase your chances of owning a BMW M3.",
                "What has the BBC come to? Toilets, that's what",
                "I don't believe that is necessarily any more dangerous than the many other risky things that people do with their free hands while driving - nose-picking, reading the paper, studying the A-Z, beating the children, and so on.",
                "I think I was once given cocaine but I sneezed so it didn't go up my nose. In fact, it may have been icing sugar."]

@client.event
async def on_ready():
    print("cursed bot")

@client.event
async def on_message(msg):
    if "boris" in msg.content.lower():
        message_to_send = random.choice(boris_quotes)
        await msg.channel.send(message_to_send)

client.run("token")
    
