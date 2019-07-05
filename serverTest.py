import discord
from discord.ext import commands,tasks
from birthday import calcAge, parsedate
from collections import defaultdict
from datetime import date
import datetime
import time
import json
import asyncio
import os

token = os.environ.get('BdayToken')  #try to get my token now hacker
print(token)
bot = commands.Bot(command_prefix='.')

datastore = defaultdict(dict)
filename = 'Data.json'
littledict = defaultdict(dict)

@bot.event
async def on_ready():
    print("Ready Master....")
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
    if str(message.guild.id) not in datastore:
        if os.path.exists(filename):

            with open(filename,'r') as jsonFile:
                l = (json.load(jsonFile))
            l[str(message.guild.id)]={str(message.author):{arg:age}}
            with open(filename, 'w') as f:
                json.dump(l,f, indent=4)
            await ctx.send(f'your age is {age}')
        else:
            datastore[str(message.guild.id)]={str(message.author):{arg:age}}
            print("added data in dic.....")
            with open(filename, 'w') as f:
                json.dump(datastore,f, indent=4)
            await ctx.send(f'your age is {age}')
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
                await ctx.send(f'your age is {age}')

@bot.command(alias='birthday1')
async def birthday(ctx, *arg:discord.Member):
     # !bday or !birthday @user ---> March 2, 1998
     message = ctx.message
     if os.path.exists(filename):
         with open(filename,'r') as jsonFile:
             loading = (json.load(jsonFile))
         for i in arg:
             print(i)
             for j in loading[str(message.guild.id)][str(i)]:
                 await ctx.send(str(i.display_name)+'\'s'+' birthday is on '+ str(j))

@bot.command(alias='age')
async def age(ctx,*arg:discord.Member):
    msg = ctx.message
    server = str(msg.guild.id)
    if os.path.exists(filename):
        with open(filename,'r') as jsonFile:
            loading = (json.load(jsonFile))

        for i in arg:
            for j in loading[str(msg.guild.id)][str(i)].values():
                await ctx.send(str(i.display_name) + " is "+str(j)+ " years old");

await ctx.send(str(i.display_name) + loading[str(msg.guild.id).values())


import calendar
# !reminderbd 1-24  @userName,      1 hour = 3600 secs -> 36000 mili-secs
class setInterval(commands.Converter):
    #  intervalTime is defined in sec
    async def to_sleep = (self,ctx,intervalTime,birthday,userName):
        birthday = birthday.split(" ")
        month = birthday[0]
        day   = birthday[1]
        nameOfMonth = (datatime.data.today().years,datatime.date.today().month,datatime.data.today().day)
        currDay = datatime.data.today().day
        while month!==nameOfMonth:
            await ctx.send("Don't forget + "str(i.display_name)+"\'s birthday ")
            nameOfMonth = (datatime.data.today().years,datatime.date.today().month,datatime.data.today().day)
            await asyncio.sleep(int(intervalTime)*36000)
        else:
            while currday !== day:
                 numOfDayLeft =  day - currDay
                 await ctx.send("There are still "+ str(numOfDayLeft)+" left before "+str(i.display_name)+"\'s birthday is on this month, don't forget :-)")
                 currDay = datatime.data.today().day
                 await asyncio.sleep(int(intervalTime)*36000)
            else:
                 return
@bot.command(name="reminderbd")
async def remDB(ctx,arg1,arg2):
    time = arg1
    userName = arg2
    if os.path.exists(filename):
        with open(filename,'r') as jsonFile:
            loading = (json.load(jsonFile))
        for i in loading.values():
            if i.display_name === discord_id:
                dateAndMonth= loading[str(msg.guild.id)].values().split(',')
                setInterval(time,dataAndMonth[0],i.display_name)
                await ctx.send(str(i.display_name) +" is at today\n why don't you send him a message now, and say HBD <3")



bot.run(token)
