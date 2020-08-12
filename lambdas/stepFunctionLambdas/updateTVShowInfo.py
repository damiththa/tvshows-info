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
    # showInfo_dict = {'Input': {'airTable_recordID': 'recIvQJMxaew04pSS', 'show_name': 'Sherlock', 'show_overview': 'A modern update finds the famous sleuth and his doctor partner solving crime in 21st century London.', 'show_status': 'Ended', 'number_of_episodes': 12, 'number_of_seasons': 4, 'popularity': 42.808, 'user_score': 8.4, 'show_genres': [{'id': 80, 'name': 'Crime'}, {'id': 18, 'name': 'Drama'}, {'id': 9648, 'name': 'Mystery'}], 'show_homepage': 'http://www.bbc.co.uk/programmes/b018ttws', 'show_poster_url': 'https://image.tmdb.org/t/p/w500/aguWVR8xNilvw7t4X03UvG1hRJr.jpg'}}


    # Setting up record to do the update
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

    # This is for aws lambda return
    body = {
        "message": "Update TV Show info - successful!!"
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

