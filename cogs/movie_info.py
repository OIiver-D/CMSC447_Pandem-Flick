import discord
from MovieFunctions import movie_functions
from discord.ext import commands
import pymongo
from pymongo import MongoClient
# from db import DB


class movie_info(commands.Cog):

    def __init__(self, client):
        self.client = client
    #    self.db = DB()

    @commands.Cog.listener()
    async def on_ready(self):
        print("movie info cog online")

#   don't really need this command
#
#    @commands.command(pass_context=True)
#    async def get_id(self, ctx, *, message):
#        movie_id = movie_functions.get_id(message)
#        await ctx.send(movie_id)

    @commands.command(pass_context=True)
    async def get_rating(self, ctx, *, message):
        movie_id = movie_functions.get_id(message)
        rating = movie_functions.get_ratings(movie_id)

        await ctx.send(f'Rating: {rating}')

    @commands.command(pass_context=True)
    async def embed(self, ctx, *, message):

        cluster = MongoClient(
             "mongodb+srv://pfAdmin:ZZ68174@cluster0.pdcfd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

        # assigns database
        db = cluster["PandemFlickBot"]

        # assigns collection (a minidatabase within the larger database)
        collection = db["movies"]

        # results = self.db.find(message)

        data = movie_functions.get_data(message)
        _id = data['results'][0]['id'][7:-1]
        web_url = 'https://www.imdb.com/title/' + _id
        image_url = data['results'][0]['image']['url']
        title = data['results'][0]['title']
        category = data['results'][0]['titleType']
        genres = movie_functions.get_genres(_id)
        genres = ", ".join(genres)
        rating = movie_functions.get_ratings(_id)
        time = data['results'][0]['runningTimeInMinutes']
        plot = movie_functions.get_plot(_id)

        movie = {"_id": data['results'][0]['id'][7:-1],
                 "title": data['results'][0]['title'],
                 "category": data['results'][0]['titleType'],
                 "genres": genres,
                 "rating": movie_functions.get_ratings(_id),
                 "web_url": 'https://www.imdb.com/title/' + _id,
                 "image_url": data['results'][0]['image']['url'],
                 "time": data['results'][0]['runningTimeInMinutes'],
                 "plot": movie_functions.get_plot(_id)
                 }
        #   self.db.insert(movie)
        collection.insert_one(movie)

        # all of the code below sets up the embed, the box that we send back to the user
        # we can change colors, etc later & change this to a function to clean up code
        # character '173' is empty character, unsure of what to put in description
        embed = discord.Embed(title=title, url=web_url, color=0xFF5733)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=image_url)
        embed.add_field(name="Plot", value=plot, inline=False)
        embed.add_field(name="Rating", value=rating, inline=True)
        embed.add_field(name="Running Time", value="{} minutes".format(time), inline=True)
        embed.add_field(name="Category", value=category, inline=True)
        embed.add_field(name="Genres", value=genres, inline=False)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(movie_info(client))
