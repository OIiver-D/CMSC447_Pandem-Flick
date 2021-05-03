import discord
from discord.ext import commands 
from discord.utils import get

class help(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="all the movies"))
        print("help cog online.")

    @commands.command(pass_context=True)    
    async def help(self,ctx):
        embed = discord.Embed(title="Pandem-Flick Commands: ", color=0xAC1ADC)
        embed.add_field(name="!addEvent mm/dd/yyyy 12:00[am/pm] [Event Name]", value=" Creates a watchtime event.\
                                 \n Example: @addEvent 5/1/2021 1:30pm Example Watch Party", inline=False)
        embed.add_field(name="!addList [Movie Title]", value=" Adds the specified movie to the users watchlist", inline=False)
        embed.add_field(name="!delList [Movie Title]", value=" Removes the specified movie to the users watchlist", inline=False)
        embed.add_field(name="!showList", value=" Displays the users watchlist to them", inline=False)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(help(client))