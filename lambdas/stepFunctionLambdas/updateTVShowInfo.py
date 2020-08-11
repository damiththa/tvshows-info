import json
import requests
import os

def handler(event, context):

    print ('we are in update lambda, triggered by step functions- woohoo')
    
    event = json.dumps(event) # getting the object returned in json 
    # print (event)

    showInfo_dict = json.loads(event)
    print (showInfo_dict)
    print (showInfo_dict['Input']['show_homepage'])

    # This is for aws lambda return
    body = {
        "message": "This is the message!"
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

