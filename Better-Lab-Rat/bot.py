import discord
from discord.ext import commands
import time
import asyncio
import sqlite3

#This is a rewrite of the Lab Rat bot used in The Labs.
#It is probably far from perfect but it's much better than the original.
#I didn't bother to rewrite reports as it would've taken too long for a little project rewriting a dead bot.
#Feel free to use this code or make changes to it.

client           = commands.Bot(command_prefix="!", case_insensitive=True)
client.flag      = ""
client.challenge = ""
client.cooldowns = []

client.remove_command("help") # remove default help command to replace with our own

"""Database Functions"""
# Preserved from original Lab Rat
# I actually liked this code until
# I switched to PostgreSQL

def execute_query(table, query):
    conn = sqlite3.connect(table) 
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    c.close()
    conn.close()

def db_query(table, query):
    conn = sqlite3.connect(table)
    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()
    c.close()
    conn.close()
    return result

def create_user(user):
    check = db_query("users.db", "SELECT user_id FROM users WHERE user_id = %s" % (user.id))
    if len(check) == 0:
        execute_query("users.db", "INSERT INTO users (user_id) VALUES (%s)" % (user.id))

"""Discord Events"""
@client.event
async def on_ready():
    print(client.user.name, client.user.id)

@client.event
async def on_message(message):
    await client.process_commands(message)
    
    if message.channel.id == 439434153629319168:
        await message.delete()

    if message.author.id in cooldowns:
        pass
    else:
        cooldowns.append(message.author.id)
        author = message.author
        current = db_query("users.db", "SELECT message_weekly FROM users WHERE user_id = '%s'" % (author.id))
        if len(current) == 0:
            create_user(author)
            current = 0
        else:
            current = current[0][0]

        new = current + 1
        execute_query("users.db", "UPDATE users SET message_weekly = %s WHERE user_id = '%s'" % (new, author.id))
        await asyncio.sleep(60)
        cooldowns.remove(message.author.id)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Invalid Syntax",
                              description=f"Usage: **!{ctx.command.usage}**",
                              color=0xFF5555)
        await ctx.send(embed=embed)

"""Custom Check"""
#Checks if the user has the 'Staff' role before they can run the command
#Better to do it with a custom check rather than the has_permissions check
#since I can get it by role name
def staff_check():
    async def predicate(ctx):
        staff_role = discord.utils.get(ctx.author.roles, name="Staff")
        if staff_role is None:
            return False
        
        return True
    return commands.check(predicate)

"""Commands"""
@client.command()
async def accept(ctx):
    if ctx.channel.id == 439434153629319168:
        role = discord.utils.get(ctx.guild.roles, name="Registered")
        role_level = discord.utils.get(ctx.guild.roles, name="Noob")
        await ctx.author.add_roles(role, role_level)

        channel = client.get_channel(439465475265658891)
        embed = discord.Embed(title="User Registered",
                              description=f"{ctx.author.name} successfully registered!",
                              color=0x55FF55)
        await channel.send(embed=embed)

        create_user(ctx.author)

@client.command()
@staff_check()
async def promotions(ctx):
    levels = db_query("users.db", "SELECT message_weekly, user_id FROM users ORDER BY message_weekly DESC")
    leaderboard = []
    for counter in range(0, 15):
        try:
            user = ctx.guild.get_member(levels[counter][1])
            if user is None:
                user_id = "N/A"
                level = levels[counter][0]
            else:
                user_id = user.mention
                level = levels[counter][0]

            leaderboard.append(f"**#{counter+1} {user_id}: Messages: {level}**")
        except IndexError:
            pass

    embed = discord.Embed(title="Possible Promotions",
                          description="\n".join(leaderboard),
                          color=0xFFAA00)
    await ctx.send(embed=embed)

@client.command(usgae="submit flag")
async def submit(ctx, *, flag: str):
    chal = client.challenge
    if flag == client.flag:
        embed = discord.Embed(title="Owned",
                              description=f"{ctx.author.name} has owned the **{chal}** challenge!",
                              color=0x55FF55)
    else:
        embed = discord.Embed(title="Invalid Flag!",
                              description="Oof! What a bummer! Try Harder!",
                              color=0xFF5555)
        
    await ctx.send(embed=embed)

# Punishment Commands
@client.command()
@staff_check()
async def lock(ctx, time: int=None):
    await ctx.message.delete()
    
    default = discord.utils.get(ctx.guild.roles, name="Registered")
    perms = default.permissions
    perms.send_messages = False
    await default.edit(permissions=perms)
    if time == None:
        embed = discord.Embed(title="Server Locked",
                              description=f"The server has been locked by {ctx.author.name}",
                              color=0xFF5555)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Server Locked",
                              description=f"The server has been locked by {ctx.author.name} for **{time} minutes**.",
                              color=0xFF5555)
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(time*60)
        perms.send_messages = True
        await default.edit(permissions=perms)
        await msg.delete()
    
@client.command()
@staff_check()
async def unlock(ctx):
    await ctx.message.delete()
    
    default = discord.utils.get(ctx.guild.roles, name="Staff")
    perms = default.permissions
    perms.send_messages=True
    await default.edit(permissions=perms)

    embed = discord.Embed(title="Server Unlocked",
                          description=f"The server has been unlocked by {ctx.author.name}",
                          color=0x55FF55)
    await ctx.send(embed=embed)

@client.command(usage="kick <member> <reason>")
@staff_check()
async def kick(ctx, member: discord.Member, *, reason: str):
    embed = discord.Embed(title="User Kicked",
                          description=f"{member.name} was kicked from The Labs by {ctx.author.name} for **{reason}**",
                          color=0xFF5555)

    user_embed = discord.Embed(title="Kicked",
                               description=f"You were kicked from The Labs by {ctx.author.name} for **{reason}**",
                               color=0xFF5555)
    await ctx.send(embed=embed)
    try:
        await member.send(embed=user_embed)
    except:
        pass

    await member.kick(reason=f"[{ctx.author.name}]: {reason}")

@client.command(usage="ban <member> <reason>")
@staff_check()
async def ban(ctx, member: discord.Member, *, reason: str):
    embed = discord.Embed(title="User Banned",
                          description=f"{member.name} was banned from The Labs by {ctx.author.name} for **{reason}**",
                          color=0xFF5555)

    user_embed = discord.Embed(title="Banned",
                               description=f"You were banned from The Labs by {ctx.author.name} for **{reason}**",
                               color=0xFF5555)
    await ctx.send(embed=embed)
    try:
        await member.send(embed=user_embed)
    except:
        pass

    await member.ban(reason=f"[{ctx.author.name}]: {reason}")
    
# Admin Commands
@client.command()
@commands.is_owner()
async def resetweekly(ctx):
    execute_query("users.id", "UPDATE users SET message_weekly = 0")

@client.command()
@commands.is_owner()
async def create_users(ctx):
    msg = await ctx.send("Creating...")
    for user in ctx.guild.members:
        create_user(user)
    await msg.edit(content="Done")

@client.command(usage="setflag <flag>")
@commands.is_owner()
async def setflag(ctx, *, flag: str):
    client.flag = flag

@client.command(usage="setchal <challenge>")
@commands.is_owner()
async def setchal(ctx, *, challenge: str):
    client.challenge = challenge

client.run('token')
