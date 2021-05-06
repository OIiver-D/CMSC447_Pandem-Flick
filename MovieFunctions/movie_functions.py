import http.client
import json
import discord
import urllib.parse
import re
from MovieFunctions import movie_functions

conn = http.client.HTTPSConnection("imdb8.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "7370d66108msh075650f3a47a6a8p148fb0jsne3f707ea2d26",
    'x-rapidapi-host': "imdb8.p.rapidapi.com"
}


# Sets up HTTPS connection
def get_data(title):
    title = urllib.parse.quote(title, safe='')
    # title = title.replace(" ", "%20")
    # title = title.replace("&", "%26")
    conn.request("GET", "/auto-complete?q=" + title, headers=headers)
    #
    # This converts json into dictionary to use in python
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    if 'd' in data.keys():
        _id = data['d'][0]['id']
        if _id[0:2] != "tt":
            _id = get_id(title)
            data['d'][0]['id'] = _id

        conn.request("GET", "/title/get-overview-details?tconst=" + _id + "&currentCountry=US",
                     headers=headers)

        res1 = conn.getresponse()

        overview = json.loads(res1.read().decode("utf-8"))
    else:
        data, overview = None, None

    return data, overview


def get_ratings(movie_id):
    conn.request("GET", "/title/get-ratings?tconst=" + movie_id, headers=headers)

    # This converts json into dictionary to use in python
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    print(data)

    if "rating" in data:
        rating = data['rating']
    else:
        rating = "N/A"

    return rating


def get_id(title):
    title = title.replace(" ", "%20")
    conn.request("GET", "/title/find?q=" + title, headers=headers)
    # This converts json into dictionary to use in python
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    movie_id = data['results'][0]['id'][7:-1]

    return movie_id


def get_genres(_id):
    conn.request("GET", "/title/get-genres?tconst=" + _id, headers=headers)
    # This converts json into dictionary to use in python
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))

    return data


def get_plot(_id):
    conn.request("GET", "/title/get-plots?tconst=" + _id, headers=headers)
    # This converts json into dictionary to use in python
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    plot = data['plots'][0]['text']

    return plot


def search(query, collection):
    # searches for movie in database first
    # search only works for titles
    # ignores case, exact match
    query1 = re.escape(query)
    results = collection.find_one({"title": {"$regex": '^' + query1 + '$', "$options": 'i'}})

    if results is None:
        data, overview = movie_functions.get_data(query)

        if data is None and overview is None:
            movie = None
        else:
            movie = assign(data, overview)

            # checks if movie id is already in database before trying to add it
            id_check = collection.find_one({'_id': movie['_id']})
            if id_check is None:
                collection.insert_one(movie)
    else:

        movie = results

    return movie

    # all of the code below sets up the embed, the box that we send back to the user
    # we can change colors, etc later & change this to function to clean up code
    # character '173' is empty character, unsure of what to put in description


def build_display(ctx, movie):
    embed = discord.Embed(title=movie['title'], url=movie['web_url'], color=0xFF5733)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    if 'image_url' in movie.keys():
        embed.set_thumbnail(url=movie['image_url'])
    embed.add_field(name="Plot", value=movie['plot'], inline=False)
    if 'rating' in movie.keys():
        embed.add_field(name="Rating", value=movie['rating'], inline=True)
    else:
        embed.add_field(name="Rating", value="N/A", inline=True)
    if 'time' in movie.keys():
        embed.add_field(name="Running Time", value="{} minutes".format(movie['time']), inline=True)
    else:
        embed.add_field(name="Running Time", value="N/A", inline=True)
    if 'category' in movie.keys():
        embed.add_field(name="Category", value=movie['category'], inline=True)
    else:
        embed.add_field(name="Category", value="N/A", inline=True)
    if 'genres' in movie.keys():
        embed.add_field(name="Genres", value=movie['genres'], inline=False)
    else:
        embed.add_field(name="Genres", value="N/A", inline=False)

    return embed


# function takes two dictionaries and extracts the needed data from them
def assign(data, overview):
    _id = data['d'][0]['id']
    movie = {"_id": _id,
             "title": overview['title']['title'],
             "web_url": 'https://www.imdb.com/title/' + _id,
             }

    if 'plotOutline' in overview.keys():
        movie['plot'] = overview['plotOutline']['text']

    if 'genres' in overview.keys():
        genres = overview['genres']
        genres = ", ".join(genres)
        movie['genres'] = genres

    if 'titleType' in overview['title'].keys():
        movie['category'] = overview['title']['titleType']

    if 'runningTimeInMinutes' in overview['title'].keys():
        movie['time'] = overview['title']['runningTimeInMinutes']

    if 'rating' in overview['ratings'].keys():
        movie['rating'] = overview['ratings']['rating']

    if 'image' in overview['title'].keys():
        movie['image_url'] = overview['title']['image']['url']

    return movie
