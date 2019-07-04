import discord
from discord.ext import commands
from birthday import calcAge, parsedate
from collections import defaultdict
from datetime import date
import datetime
import time

token = 'NTk2MDEyMjMxNjM3MDczOTIx.XRzWmw.jLuhagDih7ujgXFg_mcceaJiTxI'
bot = commands.Bot(command_prefix='!')

datastore = defaultdict(dict)

#for i in d.keys():
#    await ctx.send(d[i]) ---> 21
#{serverid : {user:{'birthday': age}}}   d=datastore[server][i]
@bot.command(alias='mybday')
# !mybday or !mybirthday March 2, 1998
async def mybirthday(ctx,*,arg):
    message = ctx.message
    print('adding birthday data....')
    date = parsedate((arg))
    age = calcAge(datetime.date(date[-1],date[-3],date[-2]))
    if message.guild.id not in datastore:
        datastore[message.guild.id]={message.author:{arg:age}}
    else:
        datastore[message.guild.id][message.author]={arg:age}
    print(datastore)
    d =datastore[message.guild.id][message.author]
    for i in d.keys():
        await ctx.send(d[i])


@bot.command(alias='birthday1')
async def birthday(ctx, *arg:discord.Member):
     # !bday or !birthday @user ---> March 2, 1998
     id = ctx.message.guild.id
     for i in arg:
         for j in datastore[id][i]:
             await ctx.send(str(i.display_name)+' birthday is on '+ str(j))
@bot.command(alias='age')
async def userAge(ctx,*arg:discord.Member):
    msg = ctx.message
    server = msg.guild
    for i in arg:
        for j in datastore[server][i].keys():
            await ctx.send(str(i.display_name) + " is "+str(j)+ " years old");
bot.run(token)
