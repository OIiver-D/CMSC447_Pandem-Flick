import discord
from discord.ext import commands, tasks 
from get_id import get_id
from get_id import get_meta
from discord.utils import get
from datetime import datetime, time, date
import http.client
import json
import random
import pymongo


# CLUSTER = os.environ.get('MONGODB_URI', None)
# cluster = pymongo.MongoClient(CLUSTER)

cluster = pymongo.MongoClient("mongodb+srv://group1:group1@cluster0.yabgb.mongodb.net/PandemFlick?retryWrites=true&w=majority")

db = cluster.Events
collection = db['Events']
class sched(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.check_event.start() 
        print("sched cog online.")

    @commands.command(pass_context=True)    
    async def addEvent(self,ctx):
        if " " in ctx.message.content:
            event_str = " ".join(ctx.message.content.split()[1:])
        #split by spaces to get the date
        curr_dt = datetime.now()
        event_str = event_str.split(" ")
        date = event_str[0]
        date_split = date.split('/')
        new_date = datetime(int(date_split[2]), int(date_split[0]), int(date_split[1]))
        currDate = datetime(curr_dt.year, curr_dt.month, curr_dt.day)
        #makes sure its a valid date
        if currDate <= new_date:
            time = event_str[1]
            tmp = time[-2:]
            if tmp == "pm":
                time.split(":")
                tmp2 = int(time[0]) + 12
                time = str(tmp2) +":"+time[2:-2]
            else:
                time = time[:-2]

            server_id = str(ctx.message.guild.id)
            # build dict to store on the database
            new_event = {
            'server_id': server_id,
            'event name': " ".join(event_str[2:]),
            'date': date,
            'time': time,
            }
            collection.insert_one(new_event)
            await ctx.send("Event '" + new_event['event name'] + "' is being added")
        else:
            await ctx.send("I didn't realize you could time travel.\nPut a date that is not in the past")


    @commands.command(pass_context=True)    
    async def delEvent(self,ctx):
        if " " in ctx.message.content:
            event_str = " ".join(ctx.message.content.split()[1:])
        # loops through all events stored on database
        for i in collection.find():
            #if an event name matches the one trying to be deleted, will delete that event
            # also makes sure the user is from the same server
            if i['event name'] == event_str and int(ctx.guild.id) == int(i['server_id']):
                await ctx.send("Event '" + i['event name'] + "' is being removed")
                collection.remove({"_id":i['_id']})



    @tasks.loop(seconds=60)
    async def check_event(self):
        await self.client.wait_until_ready()
        curr_dt = datetime.now()
        #loops through all the events stored in the database
        for i in collection.find():
            event_date = i['date']
            date_split = event_date.split('/')
            event_date = datetime(int(date_split[2]), int(date_split[0]), int(date_split[1]))
            curr_date = datetime(curr_dt.year, curr_dt.month, curr_dt.day)
            # checks to see if there is a event that is happening today
            if curr_dt.date() == event_date.date():

                # next needs to check if that event is happening within the hour
                curr_time = curr_dt.time()
                event_time = i['time'].split(':')
                hour = int(event_time[0])
                min = int(event_time[1])
                event_time = time(hour,min, 0)
                diff_time = datetime.combine(date.today(), event_time) - datetime.combine(date.today(), curr_time)
                diff_time = diff_time.total_seconds()
                
                # Creates the time difference between now and the time of the event
                diff_time = (diff_time / 60)
                # if and hour or less until the event, will send a message
                if diff_time <= 60:

                    # gets the server(guild) id from the event
                    server_id = self.client.get_guild(int(i['server_id']))
                    channel = server_id.text_channels
                    channel_found = False
                    # searches for the event-announcements channel
                    for j in range(len(channel)):
                        if channel[j].name == "event-announcements":
                            channel = self.client.get_channel(channel[j].id)
                            channel_found = True
                    # if no event announvement-channel is found, it creates one
                    if not channel_found:
                        new_channel = await server_id.categories[0].create_text_channel("event-announcements")
                        await new_channel.edit(topic = "For announcements about upcoming events")
                        channel = new_channel
                    
                    time_event = i['time'].split(':')
                    hour_event = int(time_event[0])
                    if hour_event > 12:
                        hour_event -= 12
                        am_pm = 'pm'
                    am_pm = 'am'
                    time_event = str(hour_event) + ":" + time_event[1]

                    # creates message to send to the event-announcements channel
                    embed = discord.Embed(title = i['event name'],
                                description = "This event is happening at: "+time_event + am_pm,
                                color = 0xFF0000)
                    await channel.send(embed=embed)
                    #await channel.send(server_id.default_role)
                    # removes the announced event since it won't be announced again
                    collection.remove({"_id":i['_id']})

def setup(client):
    client.add_cog(sched(client))
