import json
import requests
import os

import tmdbsimple as tmdb

TMDB_API_KEY = os.environ['TMDB_API_KEY']
tmdb.API_KEY = TMDB_API_KEY

# tmdb base url for TV
tmbd_TV_base_url = 'https://www.themoviedb.org/tv/'

# poster not found - default gif
poster_not_found_url = 'https://media.giphy.com/media/9J7tdYltWyXIY/giphy.gif'

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

    # Spy
    # tmdb_showID = 41703 
    # airTable_recordID = 'recx4qkJ6ph61Oari'

    # tv show object
    tv_show = tmdb.TV(tmdb_showID)
    res = tv_show.info()

    tv_show_info_dict = {} # dict. to hold interested attributes for THIS TV show 

    # NOTEME: making sure there is a values in attributes to avoid UPDATE errors. 

    # Show homepage url
    # If returned (from tmdb) homepage url is NULL, then directing to the page in tmdb
    if tv_show.homepage is not None: # checking a value for a homepage url
        show_homepage_url = tv_show.homepage
    else:
        show_homepage_url = tmbd_TV_base_url + str(tmdb_showID) + '-' + tv_show.name.replace(" ","-")
    # print (show_homepage_url)

    # show poster url
    if tv_show.poster_path is not None: # checking a valur for poster url
        show_poster_url = show_images_dict['secure_base_url'] + show_images_dict['poster_sizes'] + tv_show.poster_path
    else:
        show_poster_url = poster_not_found_url

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
        'show_homepage' : show_homepage_url,
        'show_poster_url' : show_poster_url
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

