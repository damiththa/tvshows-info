import json
import requests
import os

import tmdbsimple as tmdb

TMDB_API_KEY = os.environ['TMDB_API_KEY']
tmdb.API_KEY = TMDB_API_KEY

# show images
show_images_dict = {
    'secure_base_url' : 'https://image.tmdb.org/t/p/',
    'poster_sizes' : 'w500'
}

def handler(event, context):

    print ('We are getting tv show info.')

    event = json.dumps(event)
    showEntryInfo_dict = json.loads(event) # getting it as a python dict

    tmdb_showID = showEntryInfo_dict['Input']['tmdb_id']
    airTable_recordID = showEntryInfo_dict['Input']['rec_id']

    # HARDCODED: for testing
    # LetterKenny
    # tmdb_showID = 65798 
    # airTable_recordID = 'rec7v6jZMZkNflgFz'

    # Sherlock
    # tmdb_showID = 19885 
    # airTable_recordID = 'recIvQJMxaew04pSS'

    # tv show object
    tv_show = tmdb.TV(tmdb_showID)
    res = tv_show.info()

    tv_show_info_dict = {} # dict. to hold interested attributes for THIS TV show 

    # interested attributes into the dict. 
    tv_show_info_dict = {
        'airTable_recordID' : airTable_recordID,
        'show_name' : tv_show.name,
        'show_overview' : tv_show.overview,
        'show_status' : tv_show.status,
        'number_of_episodes' : tv_show.number_of_episodes,
        'number_of_seasons' : tv_show.number_of_seasons,
        'popularity' : tv_show.popularity,
        'user_score' : tv_show.vote_average,
        'show_genres' : tv_show.genres, # returns a list of dicts. 
        'show_homepage' : tv_show.homepage,
        'show_poster_url' : show_images_dict['secure_base_url'] + show_images_dict['poster_sizes'] + tv_show.poster_path # show poster url
    }
    # print (show_poster_url)
    # print (tv_show_info_dict)

    # NOTEME: There is no need to do a lambda return becuase the return of this will be the input of the other lambda.
    # # This is for aws lambda return
    # body = {
    #     "message": "Information collected from TMDB api successfully!"
    # }
    # response = {
    #     "statusCode": 200,
    #     "body": json.dumps(tv_show_info_dict)
    # }

    return tv_show_info_dict

