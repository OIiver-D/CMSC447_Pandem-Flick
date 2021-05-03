import discord
from discord.ext import commands 
from discord.utils import get
from get_id import get_id
from get_id import get_meta
import pandas as pd
import numpy as np
import pymongo
import json

cluster = pymongo.MongoClient("mongodb+srv://group1:group1@cluster0.yabgb.mongodb.net/PandemFlick?retryWrites=true&w=majority")
db = cluster.UserLists

movies_df = pd.read_csv("movies.csv")
ratings_df = pd.read_csv("ratings.csv")

#adds column with release year removed
#ex (Toy Story (1995) -> Toy Story)
movies_df['real_title'] = movies_df['title'].apply(lambda x: x[:len(x)-7])

#merge the two datasets
movies_rated_df = pd.merge(ratings_df, movies_df, on='movieId')

#avg rating for each movie
avg_ratings_df = pd.DataFrame(movies_rated_df.groupby('title')['rating'].mean())
avg_ratings_df['num_ratings'] = pd.DataFrame(movies_rated_df.groupby('title')['rating'].count())

#creates pivot table that shows all ratings for a particular movie
rec_ratings_df = movies_rated_df.pivot_table(index='userId', columns='title', values='rating')

#generates the recommendation
#returns a DataFrame sorted by closest correlation if successful
#otherwise, returns -1 on failure (ie movie not found)
def recommend(user_input):

    flag = False
    index = 0
    recommendations = []

    #find the movie in the dataset
    for i in range(len(movies_df.real_title)):
        if user_input == movies_df.real_title[i]:
            flag = True
            index = i
    
    #generate the rec
    if(flag == True):

        #pull ratings of specific movie and correlate user ratings with other movies
        temp_ratings = rec_ratings_df[movies_df.title[index]]
        np.seterr(all='ignore')
        temp_rec = rec_ratings_df.corrwith(temp_ratings)

        #sort the recommendations, drop nulls, drop movies with <100 ratings
        final_rec = pd.DataFrame(temp_rec, columns=['Correlation'])
        final_rec.dropna(inplace=True)
        final_rec.sort_values('Correlation', ascending=False)
        final_rec = final_rec.join(avg_ratings_df['num_ratings'])
        final_rec = final_rec[final_rec ['num_ratings']>100].sort_values('Correlation', ascending=False)

        #return a list with 3 recommendations
        index = 1
        while index < 4:
            recommendations.append(str(final_rec.index.values[index]))
            index += 1

        return recommendations

    else:
        return recommendations

def fix_title(title):
    fix = ", The"
    if(title.startswith("The ")):
        new_title = title[4:] + fix
        return new_title
    return title
    
def fix_recs(rec_list):
    fix = "The "
    for i in range(len(rec_list)):
        index = rec_list[i].find(",")
        if(index != -1):
            if(rec_list[i][index:].startswith(", The")):
                fixed_title = fix + rec_list[i][:index] + rec_list[i][index+5:]
                rec_list[i] = fixed_title

def embed_rec(title, rec_list):
    movie1_id = get_id(rec_list[0])
    movie2_id = get_id(rec_list[1])
    movie3_id = get_id(rec_list[2])


    rec_msg = discord.Embed(title="Since you liked '" + title + "'", color=0xFF5733)
    rec_msg.add_field(name="Why not try...", value= "1. " + rec_list[0]  + "\n2. " + rec_list[1]+ "\n3. " + rec_list[2] +
    "\n\n Use '!search' to find out more information about these movies!")

    return rec_msg

def fix_title(title):
    fix = ", The"
    if(title.startswith("The")):
        new_title = title[4:] + fix
        return new_title
    return title
    

class rec(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("rec cog online.")

    @commands.command(pass_context=True)    
    async def rec(self, ctx):

        #recommendation by title
        if " " in ctx.message.content:
            movie_title = " ".join(ctx.message.content.split()[1:])
            movie_id = get_id(movie_title)
            # Makes sure a valid movie_id was found
            if movie_id != -1:
                movie_meta = get_meta(movie_id)
                movie_title = movie_meta[movie_id]['title']['title']
            else:
                await ctx.send("Sorry, that movie cannot be found")

        #recommendation by user list
        else:
            user_id = str(ctx.message.author.id)
            #user_id = "123"

            #the user has a list
            if (user_id in db.list_collection_names()):
                
                #grabs random movie from user list
                collection = db[user_id]
                movie_data = list(collection.aggregate([{ "$sample": { "size": 1 } }]))

                #convert to json, pull movie title out of dict
                movie_data = json.dumps(movie_data)
                index = movie_data.find("movie_title")
                movie_title = movie_data[index+15:]
                index = movie_title.find('"')
                movie_title = movie_title[:index]


                
                #fixes inaccuracy in data set
                db_title = fix_title(movie_title)
                 


            #the user doesn't have a watch list
            else:
                await ctx.send("No watch list found for you. Try adding some movies with '@addList' so I can make a recommendation!")

                await ctx.send("Or you can also use '@rec 'title'' and get a recommendation from a specific movie!")
                return

        rec_list = recommend(movie_title)
        if(len(rec_list) == 0):
            #fixes inaccuracy in data set
            db_title = fix_title(movie_title)
            rec_list = recommend(db_title)
            if(len(rec_list) == 0):
                await ctx.send("Sorry! I wasn't able to find that movie.")

        fix_recs(rec_list)

        msg = embed_rec(movie_title, rec_list)
        await ctx.send(embed=msg)

        

def setup(client):
    client.add_cog(rec(client))