import json
import requests
import os

import tmdbsimple as tmdb

TMDB_API_KEY = os.environ['TMDB_API_KEY']
tmdb.API_KEY = TMDB_API_KEY

def handler(event, context):

    # HARDCODED: 
    # showID = 65798 # LetterKenny
    showID = 19885 # Sherlock


    tv_show = tmdb.TV(showID)
    res = tv_show.info()

    # interested attributes
    show_name = tv_show.name
    show_overview = tv_show.overview
    show_status = tv_show.status
    number_of_episodes = tv_show.number_of_episodes
    number_of_seasons = tv_show.number_of_seasons
    popularity = tv_show.popularity
    user_score = tv_show.vote_average
    show_genres = tv_show.genres # returns a list of dicts. 

    print (popularity, user_score)


    # TODO: make this more meaningful
    # This is for aws lambda return
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

