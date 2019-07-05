import discord
from discord.ext import commands,tasks
from birthday import calcAge, parsedate,birthAlert
from collections import defaultdict
from datetime import date
import datetime
import time
import json
import asyncio
import os

token = os.environ.get('BdayToken')  #try to get my token now hacker
bot = commands.Bot(command_prefix='.')

datastore = defaultdict(dict)
filename = 'Data.json'
littledict = defaultdict(dict)


@bot.event
async def on_ready():
    print("Ready Master....")


#{serverid : {user:{'birthday': age}}}   d=datastore[server][i]
# !mybday or !mybirthday March 2, 1998
@bot.command(aliases=['mybday','enter'])
async def mybirthday(ctx,*,arg):
    message = ctx.message
    print('adding birthday data....')
    date = parsedate((arg))
    age = calcAge(datetime.date(date[-1],date[-3],date[-2]))
    if str(message.guild.id) not in datastore:
        if os.path.exists(filename):

            with open(filename,'r') as jsonFile:
                l = (json.load(jsonFile))
            l[str(message.guild.id)]={str(message.author):{arg:age}}
            with open(filename, 'w') as f:
                json.dump(l,f, indent=4)
            await ctx.send(f'{message.author.display_name} birthday is now in the Database')
        else:
            datastore[str(message.guild.id)]={str(message.author):{arg:age}}
            print("added data in dic.....")
            with open(filename, 'w') as f:
                json.dump(datastore,f, indent=4)
            await ctx.send(f'``{message.author.display_name}`` birthday is now ``in`` the Database')
            print('exiting ready....')
    else:
        if os.path.exists(filename):
            with open(filename,'r') as jsonFile:
                l = (json.load(jsonFile))
            l[str(message.guild.id)][str(message.author)]={arg:age}
            print(datastore)
            d =l[str(message.guild.id)][str(message.author)]
            with open(filename, 'w') as f:
                json.dump(l,f, sort_keys=True,indent=4)
            for i in d.keys():
                await ctx.send(f'``{message.author.display_name}`` birthday is now ``in`` the Database')
            print('stored in Json....')

@bot.command( aliases = ['birth','born'])
async def birthday(ctx, *arg:discord.Member):
     # !bday or !birthday @user ---> March 2, 1998
     message = ctx.message
     if os.path.exists(filename):
         with open(filename,'r') as jsonFile:
             loading = (json.load(jsonFile))
         for i in arg:
             print(i)
             if i in loading[str(message.guild.id)][str(i)]:
                 for j in loading[str(message.guild.id)][str(i)]:
                     await ctx.send('``'+str(i.display_name)+'``\'s'+' birthday is on ``'+ str(j)+'``')
             else:
                await ctx.send('please put your birthday for example : ``.mybday March 2, 1998`` ')

@bot.command(aliases=['myAge','myage'])
async def meage(ctx):
    message = ctx.message
    if os.path.exists(filename):
        with open(filename,'r') as jsonFile:
            loading = (json.load(jsonFile))
        birth = loading[str(message.guild.id)][str(message.author)]
        for i in birth:
            await ctx.send(f'Your age is ``{birth[i]}``')

@bot.command(aliases=['snow','dude','maker'])
async def author(ctx,*arg):
    birth = 'March 2, 1998'
    date = parsedate((birth))
    age = calcAge(datetime.date(date[-1],date[-3],date[-2]))
    for i in arg:
        if i== 'age':
            await ctx.send(f'Snow\'s is ``{age}`` years old')
        elif i == 'born' or i == 'birthday' or i == 'birth':
            await ctx.send(f'Snow\'s birthday is on ``{birth}`` ')
        else:
            await ctx.send('give the comman these arguments: ``age``,  ``born``, ``birth``')



@bot.command(aliases=['old'])
async def age(ctx,*arg:discord.Member):
    msg = ctx.message
    server = str(msg.guild.id)
    if os.path.exists(filename):
        with open(filename,'r') as jsonFile:
            loading = (json.load(jsonFile))

        for i in arg:
            for j in loading[str(msg.guild.id)][str(i)].values():
                await ctx.send(str(i.display_name) + " is ``"+str(j)+ "`` years old");


@tasks.loop(hours=12)
async def bdayReminder():
    if os.path.exists(filename):
        with open(filename,'r') as jsonFile:
            loading = (json.load(jsonFile))
        for server in loading:
            for user in loading[server]:
                print(user)
                for birth in loading[server][user]:
                    print(birth)
                    if birthAlert(str(birth)):
                        print(user)
                        id = int(server)
                        print(type(id), id)
                        channels = bot.get_guild(id).text_channels
                        age = 0
                        for i in loading[server][user]:
                            age =loading[server][user][i]
                        # print(int(server))
                        for channel in channels:
                            await channel.send(f'@here Happy ``{age}`` birthday to ``{user}``! ')
@bdayReminder.before_loop
async def test():
    print('waiting...')
    await bot.wait_until_ready()

bdayReminder.start()



bot.run(token)
