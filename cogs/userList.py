import discord
from discord.ext import commands 
from get_id import get_id
from get_id import get_meta
from discord.utils import get
import http.client
import json
import random
import pymongo


cluster = pymongo.MongoClient("mongodb+srv://group1:group1@cluster0.yabgb.mongodb.net/PandemFlick?retryWrites=true&w=majority")
db = cluster.UserLists
class userList(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("userList cog online.")

    @commands.command(pass_context=True)    
    async def addList(self,ctx):
        if " " in ctx.message.content:
            movie_title = " ".join(ctx.message.content.split()[1:])
            #call getData from getData.py 
            movie_id = get_id(movie_title)
            # Makes sure a valid movie_id was found
            if movie_id != -1:
                #Check the movie id with the database to see if it's already in the users watchlist
                user_id = str(ctx.message.author.id)
                collection = db[user_id]
                if collection.count_documents({'_id': movie_id}) == 0:
                    movie_meta = get_meta(movie_id)
                    movie_info = {
                        "_id": movie_id,
                        "movie_title": movie_meta[movie_id]['title']['title'] ,
                        "genre": movie_meta[movie_id]['genres'][0]
                    }

                    collection.insert_one(movie_info)
                    await ctx.send("adding `"+movie_info['movie_title']+"` to user list")
                else:
                    await ctx.send("Sorry, that movie is already on your watch list")
            else:
                await ctx.send("Sorry, that movie cannot be found")
        else:
            await ctx.send("Please specify what movie you want to add")


    @commands.command(pass_context=True)    
    async def delList(self,ctx):
        if " " in ctx.message.content:
            movie_title = " ".join(ctx.message.content.split()[1:])
            user_id = str(ctx.message.author.id)
            collection = db[user_id]
            #call getData from getData.py 
            movie_id = get_id(movie_title)
            if movie_id != -1:
                for i in collection.find():
                    if i['_id'] == movie_id:
                        movie_title = i['movie_title']
                        collection.delete_one(i)
                        await ctx.send("Deleting `"+movie_title+"`from user list")
            else:
                await ctx.send("That movie was not in your list")
        else:
            await ctx.send("Please specify what movie you want to add")

    @commands.command(pass_context=True)    
    async def showList(self,ctx):
        user_id = str(ctx.message.author.id)
        collection = db[user_id]
        movies = ""
        movie_num = 1
        for i in collection.find():
            movies += str(movie_num) +": " +i['movie_title']+"\n"
            movie_num += 1
        embed = discord.Embed(title = ctx.message.author.display_name +"'s Movie List",
                                description = movies,
                                color = 0xFF0000)
        await ctx.send(embed=embed)
def setup(client):
    client.add_cog(userList(client))