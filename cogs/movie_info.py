import pymongo
from discord.ext import tasks, commands
from discord.ext.commands import MissingRequiredArgument
from MovieFunctions import movie_functions
from discord.ext import commands
from pymongo import MongoClient


class movie_info(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("movie info cog online")

    @commands.command(pass_context=True)
    async def info(self, ctx, *, message):

        cluster = pymongo.MongoClient(
            "mongodb+srv://group1:group1@cluster0.yabgb.mongodb.net/PandemFlick?retryWrites=true&w=majority")

        # assigns database
        db = cluster.MovieCache

        # assigns collection (a minidatabase within the larger database)
        collection = db["movies"]

        movie = movie_functions.search(message, collection)
        embed = movie_functions.build_display(ctx, movie)
        
        if movie is None:
            await ctx.send("Your search returned no results.")
        else:
            embed = movie_functions.build_display(ctx, movie)
            await ctx.send(embed=embed)


    @info.error
    async def info_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Please format your command correctly. !info \"Movie Title\"")
        else:
            await ctx.send(error)


def setup(client):
    client.add_cog(movie_info(client))
