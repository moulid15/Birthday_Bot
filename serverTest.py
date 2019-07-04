import discord
from discord.ext import commands
from birthday import calcAge, parsedate
from collections import defaultdict

token = 
bot = commands.Bot(command_prefix='!')

datastore = defaultdict(dict)
#for i in b.keys():
#    await ctx.send(b[i]) ---> 21
#{serverid : {user:{'birthday': age}}}   b=d[sID][user] ''
@bot.command(alias='mybday','mybirthday')
# !mybday or !mybirthday March 2, 1998
async def mybirthday(ctx,*,arg):



@bot.command(alias='birthday','bday')
async def birthday(ctx, arg:discord.Member):
     # !bday or !birthday @user ---> March 2, 1998
     for i in arg:
         ctx.send('{i.display_name} birthday is on {d[i]}')
