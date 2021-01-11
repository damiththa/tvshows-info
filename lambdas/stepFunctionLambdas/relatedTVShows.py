import json
import requests
import os

import tmdbsimple as tmdb

from datetime import datetime

# tmdb
TMDB_API_KEY = os.environ['TMDB_API_KEY']
tmdb.API_KEY = TMDB_API_KEY

# AirTable
AIRTABLE_URL = os.environ['AIRTABLE_URL']
AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
BASE_KEY = os.environ['BASE_KEY']
TBL_TV_SHOWS = os.environ['TBL_TV_SHOWS']
TBL_RELATED_TV_SHOWS = os.environ['TBL_RELATED_TV_SHOWS']

# HARDCODED: for testing
# Spy
# tmdb_showID = 41703 

cutoff_years = 3 # How old a show can be 

# Getting TV show already in related 
def getShowsAlreadyInList():
    # Getting Shows (ShowIDs) in Related Shows table
    url = AIRTABLE_URL + BASE_KEY + '/' + TBL_RELATED_TV_SHOWS
    headers = {
        'Authorization': AIRTABLE_API_KEY,
        'Content-Type' : 'application/json'
    }

    # doing GET
    res = requests.get(url, headers=headers)
    # print (res.status_code)
    # print (res.content)

    rtn = json.loads(res.content)

    showsAlreadyInList_lst = [] # Lis0t to hold shows already in list

    # looping over records
    for rec in rtn['records']:
        # print (rec['fields']['tmdbID'])
        showsAlreadyInList_lst.append(rec['fields']['tmdbID']) # append to the list

    # print (showsAlreadyInList_lst)

    return showsAlreadyInList_lst

def handler(event, context):

    event = json.dumps(event) # getting the object returned in json 
    tmdbData_dict = json.loads(event)
    
    tmdb_showID = tmdbData_dict['Input']['show_tmdbID']

    tv_show = tmdb.TV(tmdb_showID)
    similarTVShows = tv_show.similar()
    similarTVShows_results = similarTVShows['results']
    # print (similarTVShows)

    # Counting number of objects in the result
    if similarTVShows['total_results'] != 0 :  # making sure there is a valid return
        # print (similarTVShows_results)

        showsAlreadyInList_lst = getShowsAlreadyInList() # getting shows that are already in the list
        
        similarShowInfo_dict = {} # dict to hold info. about the returned similar show
        similarShows_lst = [] # list to hold similarShowInfo_dict 

        for similarShowID in similarTVShows_results:
            # print (similarShowID['id'])

            # making sure THIS show is NOT in the list already
            # NOTEME: This is to avoid duplicate entries in the table
            if similarShowID['id'] not in showsAlreadyInList_lst :

                if len(similarShows_lst) < 9 : # to POST only 10 objects at a time, per AirTable POST restriction
                
                    # from the list only interested in shows that are cutoff_years years older than current year            
                    if datetime.today().year - int(similarShowID['first_air_date'][:4]) <  cutoff_years :

                        similarShowInfo_dict = {
                            "fields": {
                                "tmdbID": similarShowID['id'],
                                "TV show name": similarShowID['name'],
                                "Show Desc.": similarShowID['overview'],
                                "First Air Date": similarShowID['first_air_date']
                            }
                        }

                        # print (similarShowInfo_dict)
                        similarShows_lst.append(similarShowInfo_dict) # append to the list
                else:
                    break
        
        # print (similarShows_lst)

        # making sure there are Shows to be posted
        if len(similarShows_lst) != 0:
            # POSTING to AirTable
            url = AIRTABLE_URL + BASE_KEY + '/' + TBL_RELATED_TV_SHOWS
            headers = {
                'Authorization': AIRTABLE_API_KEY,
                'Content-Type' : 'application/json'
            }
            payload = {
                "records" : similarShows_lst
            }
            # print (json.dumps(payload))

            # doing POST
            res = requests.post(url, headers=headers, data=json.dumps(payload))
            print (res.status_code)
            print (res.content)

            if res.status_code == 200:
                print (f'Woot Woot - {len(similarShows_lst)} show(s) successfully added to related TV shows table.')
            
        else:
            print (f'Sorry, eventhough there are similar shows but none of them made the {cutoff_years} year cutoff period.')
    
    else:
        print ('No similar shows returned for this TV show') 

    return 'Change me later'