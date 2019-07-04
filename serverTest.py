import discord
from discord.ext import commands
from birthday import calcAge, parsedate
from collections import defaultdict

token = 'NTk2MDEyMjMxNjM3MDczOTIx.XRzWmw.jLuhagDih7ujgXFg_mcceaJiTxI'
bot = commands.Bot(command_prefix='!')

datastore = defaultdict(dict)
#for i in b.keys():
#    await ctx.send(b[i]) ---> 21
# DIC -:  {serverid : {user:{'birthday': age}}}   b=d[sID][user] ''
# @bot.command(alias='mybday','mybirthday')
# # !mybday or !mybirthday March 2, 1998
# async def mybirthday(ctx,*,arg):


# !age -> get user age
@bot.command(alias='age')
async def userAge(ctx,*arg:discord.Member):
    msg = ctx.message
    server = msg.guild
    for i in arg:
        for j in datastore[server][i].keys()):
            await ctx.send(str(i.display_name) + " is "+str(j)+ " years old");
bot.run(token);
