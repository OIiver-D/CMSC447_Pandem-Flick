import discord
from discord.ext import commands 
from discord.utils import get
import pandas as pd
import numpy as np
import pymongo

cluster = pymongo.MongoClient("mongodb+srv://group1:group1@cluster0.yabgb.mongodb.net/PandemFlick?retryWrites=true&w=majority")
db = cluster.UserLists

user_id = "140511141062246400"
collection = db[user_id]
movie = list(collection.aggregate([{ "$sample": { "size": 1 } }]))
movie = movie[0]
print(movie['movie_title'])

movies_df = pd.read_csv("movies.csv")
ratings_df = pd.read_csv("ratings.csv")

print(movies_df.head())

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

        #return that DataFrame with recommendations
        return final_rec

    #the movie couldnt be found in the dataset
    else:
        return -1


class rec(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("rec cog online.")

    @commands.command(pass_context=True)    
    async def rec(self, ctx):
        print()
        

def setup(client):
    client.add_cog(rec(client))