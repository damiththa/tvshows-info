import json
import requests
import os

AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
BASE_KEY = os.environ['BASE_KEY']

def handler(event, context):

    print ('we are in update lambda, triggered by step functions- woohoo')
    
    event = json.dumps(event) # getting the object returned in json 
    # print (event)

    showInfo_dict = json.loads(event)
    # print (showInfo_dict)
    # print (showInfo_dict['Input']['show_homepage'])

    # # HARDCODED: for testing
    # showInfo_dict = {'Input': {'airTable_recordID': 'recoRLM7OoZ8cjUfI', 'show_tmdbID': '81292', 'show_name': 'Messiah', 'show_overview': 'A wary CIA officer investigates a charismatic man who sparks a spiritual movement and stirs political unrest. Who exactly is he? And what does he want?', 'show_status': 'Canceled', 'number_of_episodes': 10, 'number_of_seasons': 1, 'popularity': 18.021, 'user_score': 7.4, 'show_genres': [{'id': 18, 'name': 'Drama'}], 'show_homepage': 'https://www.netflix.com/title/80117557', 'show_poster_url': 'https://image.tmdb.org/t/p/w500/psem2jK9GGC0g7dcjb4N5SCYb1u.jpg'}}

    # dict to hold tmdb data to pass to other lambda
    tmdb_data_dict = {
        "show_tmdbID" : showInfo_dict['Input']['show_tmdbID'] # show tmdb ID
    } 

    # Setting up record to do the airtable update
    showRecodEntry = {
      "id": showInfo_dict['Input']['airTable_recordID'],
      "fields": {
        "Name": showInfo_dict['Input']['show_name'],
        "Overview": showInfo_dict['Input']['show_overview'],
        "Show status": showInfo_dict['Input']['show_status'],
        "Episodes / Seasons": str(showInfo_dict['Input']['number_of_episodes']) + ' / ' + str(showInfo_dict['Input']['number_of_seasons']),
        "Show rating": round(showInfo_dict['Input']['user_score']/2,0), # dividing by 2 and rounding to get a value out of 5
        "Home page": showInfo_dict['Input']['show_homepage'],
        "Poster": [
            {
            "url": showInfo_dict['Input']['show_poster_url'],
            "filename": showInfo_dict['Input']['show_name'] + '_poster'
            }
        ],
        "Genres": [g['name'] for g in showInfo_dict['Input']['show_genres']] # using list comprehension. See--> https://stackoverflow.com/a/7271523/789782
      }
    }

    url = 'https://api.airtable.com/v0/' + BASE_KEY + '/TV%20Shows'
    headers = {
        'Authorization': AIRTABLE_API_KEY,
        'Content-Type' : 'application/json'
    }
    payload = {
        "records" : [showRecodEntry],
        "typecast": True # NOTEME: needed for INVALID_MULTIPLE_CHOICE_OPTIONS see airtable docs.
    }

    # doing PATCH
    res = requests.patch(url, headers=headers, data=json.dumps(payload))
    # print (res.status_code)
    # print (res.content)

    if (res.status_code) == 200:
        print ('TV show update was a success !!!')
    else:
        print ('TV show update was unsuccessful !!!')

    # NOTEME: There is no need to do a lambda return becuase the return of this will be the input of the other lambda.
    # # This is for aws lambda return
    # body = {
    #     "message": "Update TV Show info - successful!!"
    # }
    # response = {
    #     "statusCode": 200,
    #     "body": json.dumps(body)
    # }

    return tmdb_data_dict

