import http.client
import string
import json

conn = http.client.HTTPSConnection("imdb8.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "7370d66108msh075650f3a47a6a8p148fb0jsne3f707ea2d26",
    'x-rapidapi-host': "imdb8.p.rapidapi.com"
}


# Sets up HTTPS connection
def get_data(title):

    title = title.replace(" ", "%20")
    conn.request("GET", "/title/find?q=" + title, headers=headers)
    # This converts json into dictionary to use in python
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    # print(data)
    movie_id = data['results'][0]['id'][7:-1]

    return data


def get_ratings(movie_id):

    conn.request("GET", "/title/get-ratings?tconst=" + movie_id, headers=headers)

    # This converts json into dictionary to use in python
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    print(data)
    rating = data['rating']
    # print(rating)

    return rating


def get_id(title):
    
    title = title.replace(" ", "%20")
    conn.request("GET", "/title/find?q=" + title, headers=headers)
    # This converts json into dictionary to use in python
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    # print(data)
    movie_id = data['results'][0]['id'][7:-1]

    return movie_id


def get_genres(_id):
 
    conn.request("GET", "/title/get-genres?tconst=" + _id, headers=headers)
    # This converts json into dictionary to use in python
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
   # print(data)

    return data


def get_plot(_id):


    conn.request("GET", "/title/get-plots?tconst=" + _id, headers=headers)
    # This converts json into dictionary to use in python
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    print(data)
    plot = data['plots'][0]['text']

    return plot


