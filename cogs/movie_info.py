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
    async def embed(self, ctx, *, message):

        cluster = MongoClient(
            "mongodb+srv://pfAdmin:ZZ68174@cluster0.pdcfd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

    async def info(self, ctx, *, message):
        cluster = MongoClient(
            "mongodb+srv://pfAdmin:ZZ68174@cluster0.pdcfd.mongodb.net/PandemFlickBot?retryWrites=true&w=majority")

        # assigns database
        db = cluster["PandemFlickBot"]

        # assigns collection (a minidatabase within the larger database)
        collection = db["movies"]

        movie = movie_functions.search(message, collection)
        embed = movie_functions.build_display(ctx, movie)

        await ctx.send(embed=embed)

    @info.error
    async def info_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Please format your command correctly. @info \"Movie Title\"")
        else:
            await ctx.send(error)


def setup(client):
    client.add_cog(movie_info(client))
