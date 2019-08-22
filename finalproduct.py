import discord
from discord.ext import commands,tasks
from birthday import calcAge, parsedate,birthAlert,dateDiffer
from collections import defaultdict
from datetime import date
import datetime
import time
import json
import asyncio
import os

token = os.environ.get('BdayToken') #try to get my token now hacker
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
    Truth = True
    date = parsedate((arg))
    age = calcAge(datetime.date(date[-1],date[-3],date[-2]))
    if os.path.exists(filename):
        print('adding birthday data....')
        with open(filename,'r') as jsonFile:
            l = (json.load(jsonFile))
        if str(message.guild.id) in l:
            for i in l[str(message.guild.id)]:
                for j in i:
                    if str(message.author) in i:
                        print(i[str(message.author)])
                        i[str(message.author)] = {arg:age}
                        print(i)
                        Truth = False
                        break
            if Truth:
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


@bot.command( aliases = ['birth'])
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
async def born(ctx):
    message = ctx.message
    user = message.author
    truth = False
    if os.path.exists(filename):
     with open(filename,'r') as jsonFile:
         loading = (json.load(jsonFile))
         for j in loading[str(message.guild.id)]:
             if str(user) in j:
                 truth = True
                 for k in j:
                     for h in j[str(k)].keys():
                         await ctx.send('``'+'Your'+'``\'s'+' birthday is on ``'+ str(h)+'``')
         if not truth:
             await ctx.send('You are not in the database. please put your birthday for example : ``.mybday March 2, 1998`` ')

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

@bot.command(aliases =['agedifference','difference', 'dif','far'])
async def length(ctx, arg:discord.Member):
    other = arg
    msg = ctx.message
    yourBirth = ''
    otherBirth = ''
    l =[]
    server = str(msg.guild.id)
    if os.path.exists(filename):
        with open(filename,'r') as jsonFile:
            loading = (json.load(jsonFile))

        for j in loading[str(msg.guild.id)]:
            if str(other) in j:
                for k in j:
                    for i in j[str(k)].keys():
                        otherBirth = i

        for j in loading[str(msg.guild.id)]:
            if str(msg.author) in j:
                for k in j:
                    for i in j[str(k)].keys():
                        yourBirth = i
        birthDiff = dateDiffer(yourBirth, otherBirth)
        if birthDiff < 0 :
            await ctx.send(f'I am ``{abs(birthDiff)}``  days older than ``{other.display_name}``')
        else:
            await ctx.send(f'`{other.display_name}`  is ``{abs(birthDiff)}`` days older than me')

    # print(l[0][(msg.author)].keys())



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



@tasks.loop(hours=13)
async def bdayReminder():
    if os.path.exists(filename):
        with open(filename,'r') as jsonFile:
            loading = (json.load(jsonFile))
        for server in loading:
            for obj in loading[server]:
                for user in obj:
                    # print(user)
                    for birth in obj[user]:
                        print(birth)
                        if birthAlert(str(birth)):
                            print('in this ')
                            id = int(server)
                            channels = bot.get_guild(id).text_channels
                            age = 0
                            com = 0
                            max = ''
                            print(len(loading[server]))
                            # print(f'this is array{loading[server][0][user][birth]}')
                            for i in range(len(loading[server])):
                                if user in loading[server][i]:
                                    print('were in')
                                    date = parsedate((birth))
                                    age = calcAge(datetime.date(date[-1],date[-3],date[-2]))
                                    loading[server][i][user][birth] = age
                            with open(filename, 'w') as f:
                                json.dump(loading,f, indent=4)
                            for channel in channels:
                                messages = await channel.history(limit=None).flatten()
                                if com < len(messages):
                                    max = channel.name
                                    com = len(messages)
                                    print(com)
                            for channel in channels:
                                print('passed')
                                if channel.name.lower() == max:
                                    await channel.send(f'@here Happy ``{age}`` birthday to ``{user}``! ')
@bdayReminder.before_loop
async def test():
    print('waiting...')
    await bot.wait_until_ready()

bdayReminder.start()



bot.run(token)
