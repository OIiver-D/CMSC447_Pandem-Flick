import http.client
import string
import json
import os
#Sets up HTTPS connection
def get_id(title):
    conn = http.client.HTTPSConnection("imdb8.p.rapidapi.com")
    IMDb_tok = os.environ.get('IMDb')
    headers = {
        'x-rapidapi-key': IMDb_tok,
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
        }
    title=title.replace(" ", "%20")
    conn.request("GET", "/title/find?q="+title, headers=headers)
    # This converts json into dictionry to use in python
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    movie_id = data['results'][0]['id'][7:-1]
    return movie_id
