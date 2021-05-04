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

        embed = discord.Embed(title="Pandem-Flick: ", color=0xAC1ADC)
        embed = discord.Embed(title="Pandem-Flick Commands: ", color=0xAC1ADC)
        embed.add_field(name="!info [Movie Title]",value="Retrieves and displays information about a specified movie.\
                            \n Example: @!info [Movie]",inline=False)

        embed.add_field(name="!addEvent mm/dd/yyyy 12:00[am/pm] [Event Name]", value=" Creates a watchtime event.\
                            \n Example: @addEvent 5/1/2021 1:30pm Example Watch Party", inline=False)

        embed.add_field(name="!delEvent [Event Name]", value=" Deletes a watch time event.\
                            \n Example: @delEvent Example Watch Party", inline=False)     

        embed.add_field(name="!addList [Movie Title]", value=" Adds the specified movie to the users watchlist\
                            \n Example: !addList Harry Potter", inline=False)

        embed.add_field(name="!delList [Movie Title]", value=" Removes the specified movie to the users watchlist\
                            \n Example: !delList Harry Potter", inline=False)

        embed.add_field(name="!showList", value=" Displays the users watchlist to them\
                            \n Example: !showList ", inline=False)

        embed.add_field(name="!addServerList [Movie Title]", value=" Adds the specified movie to the server watchlist\
                            \n Example: !addServerList Harry Potter", inline=False)

        embed.add_field(name="!delServerList [Movie Title]", value=" Removes the specified movie to the server watchlist\
                            \n Example: !delServerList Harry Potter", inline=False)

        embed.add_field(name="!showServerList", value=" Displays the server watchlist to them \
                            \n Example: !showServerList ", inline=False)

        embed.add_field(name="!rec [Movie Title*]", value=" Recommends a movie to the user based off of a movie specified. \
                            \n Movie title is optional, leave blank to get a recommendation from your user list\
                            \n Example: !rec [Movie Titile] | !rec", inline=False)


        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(help(client))