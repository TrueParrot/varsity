@bot.command()
async def clear(ctx):
    '''
    Clear messages from channel
    Usage: !clear {mention} <amount>

    Assign role permissions by entering the name of the role you want to access
    the command in "<role name here>" for example "Moderator"

    '''
    if "<role name here>" in [role.name for role in ctx.author.roles]:
        args = ctx.message.content.split()
        if len(args) < 2: #No args given
            await ctx.send("Invalid Usage; Usage: `!clear {mention} <amount>")
        else:                
            if len(args) == 2: #No specified target
                target = None
                amount = args[1]
            else:
                target = discord.utils.get(ctx.guild.members, mention=args[1])
                amount = args[2]

            def check(m):
                return m.author == target or target == None #If there is no target will always return true and delete message

            deleted = await ctx.message.channel.purge(limit=amount, check=check) #Iterates through messages and deletes the message if check returns true. Stores deleted message objects in Array.
            await ctx.send("Successfully deleted %s messages!" % (str(len(deleted))))
    else:
        await ctx.send("You do not have permission for this")
