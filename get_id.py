import http.client
import string
import json
import os

IMDB_KEY = os.environ.get('IMDb', None)
#Sets up HTTPS connection
conn = http.client.HTTPSConnection("imdb8.p.rapidapi.com")
headers = {
    'x-rapidapi-key': IMDB_KEY,
    'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

def get_id(title):
    title=title.replace(" ", "%20")
    conn.request("GET", "/title/find?q="+title, headers=headers)
    # This converts json into dictionry to use in python
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    movie_id = data['results'][0]['id'][7:-1]
    if movie_id[0] == 'm':
            return -1
    return movie_id

def get_meta(movie_id):
    conn.request("GET", "/title/get-meta-data?ids="+movie_id, headers=headers)

    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    return data
