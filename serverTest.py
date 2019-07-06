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

datastore = defaultdict(list)
filename = 'Data.json'
littledict = defaultdict(list)


@bot.event
async def on_ready():
    print("Ready Master....")


#{serverid : [{user:{'birthday': age}}},{user:{'birthday': age}}]   d=datastore[server][i]
# !mybday or !mybirthday March 2, 1998
@bot.command(aliases=['mybday','enter'])
async def mybirthday(ctx,*,arg):
    message = ctx.message

    date = parsedate((arg))
    age = calcAge(datetime.date(date[-1],date[-3],date[-2]))
    if os.path.exists(filename):
        print('adding birthday data....')
        with open(filename,'r') as jsonFile:
            l = (json.load(jsonFile))
        if str(message.guild.id) in l:
            l[str(message.guild.id)].append({str(message.author):{arg:age}})
        else:
            l[str(message.guild.id)]=[{str(message.author):{arg:age}}]
        with open(filename, 'w') as f:
            json.dump(l,f, sort_keys=True,indent=4)
        await ctx.send(f'{message.author.display_name} birthday is now in the Database')
        print('stored in Json....')
    else:
        datastore[str(message.guild.id)]=[({str(message.author):{arg:age}})]
        print("added data in dic.....")
        with open(filename, 'w') as f:
            json.dump(datastore,f, indent=4)
        await ctx.send(f'``{message.author.display_name}`` birthday is now ``in`` the Database')
        print('exiting ready....')


@bot.command( aliases = ['birth','born'])
async def birthday(ctx, *arg:discord.Member):
     # !bday or !birthday @user ---> March 2, 1998
     message = ctx.message
     truth = False
     if os.path.exists(filename):
         with open(filename,'r') as jsonFile:
             loading = (json.load(jsonFile))
         for i in arg:
             for j in loading[str(message.guild.id)]:
                 if str(i) in j:
                     truth = True
                     for k in j:
                         for h in j[str(k)].keys():
                             await ctx.send('``'+str(i.display_name)+'``\'s'+' birthday is on ``'+ str(h)+'``')
             if not truth:
                 await ctx.send('this person is not in the database. please put your birthday for example : ``.mybday March 2, 1998`` ')
@bot.command()
async def testing(ctx):
    await ctx.send('.mybirthday March 20,1980')

@bot.command(aliases=['myAge','myage'])
async def meage(ctx):
    message = ctx.message
    birth = 0
    if os.path.exists(filename):
        with open(filename,'r') as jsonFile:
            loading = (json.load(jsonFile))
        for j in loading[str(message.guild.id)]:
            if str(message.author) in j:
                for k in j:
                    for h in j[str(k)].values():
                        birth=h

        await ctx.send(f'Your age is ``{birth}``')

@bot.command(aliases=['snow','dude','maker'])
async def author(ctx,*arg):
    birth = 'March 2, 1998'
    date = parsedate((birth))
    age = calcAge(datetime.date(date[-1],date[-3],date[-2]))
    for i in arg:
        if i== 'age':
            await ctx.send(f'Snow is ``{age}`` years old')
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
            for j in loading[str(msg.guild.id)]:
                if str(i) in j:
                    for k in j:
                        for h in j[str(k)].values():
                            await ctx.send(str(i.display_name) + " is ``"+str(h)+ "`` years old");


@tasks.loop(hours=12)
async def bdayReminder():
    if os.path.exists(filename):
        with open(filename,'r') as jsonFile:
            loading = (json.load(jsonFile))
        for server in loading:
            for obj in loading[server]:
                for user in obj:
                    for birth in obj[user]:
                        if birthAlert(str(birth)):
                            id = int(server)

                            channels = bot.get_guild(id).text_channels
                            age = 0
                            print(obj[user])
                            for i in obj[user].values():
                                age =i
                            for channel in channels:
                                print('passed')
                                await channel.send(f'@here Happy ``{age}`` birthday to ``{user}``! ')
@bdayReminder.before_loop
async def test():
    print('waiting...')
    await bot.wait_until_ready()

bdayReminder.start()



bot.run(token)
