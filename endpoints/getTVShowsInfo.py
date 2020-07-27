import json
import requests
import os

import tmdbsimple as tmdb

TMDB_API_KEY = os.environ['TMDB_API_KEY']
tmdb.API_KEY = TMDB_API_KEY

def handler(event, context):
    
    movie = tmdb.Movies(603)
    res = movie.info()

    print (movie.title)




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

