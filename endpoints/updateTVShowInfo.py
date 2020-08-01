import json
import requests
import os

def handler(event, context):

    print ('fhfhfhfhfhffh')
    event = json.loads(event)
    print (event)

    # This is for aws lambda return
    body = {
        "message": "This is the message!"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

