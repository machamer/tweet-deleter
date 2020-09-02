import os
import json
import urllib3
import boto3
import uuid

def getTweets():
    http = urllib3.PoolManager()
    headers = urllib3.util.make_headers(
        basic_auth=os.environ['consumerKey'] + ':' + os.environ['consumerSecret'])
    response = http.request(
        'POST', 
        'https://api.twitter.com/oauth2/token?grant_type=client_credentials', 
        headers=headers 
    )
    json_response = json.loads(response.data)
    token = json_response['access_token']

    tweets = http.request(
        'GET',
        'https://api.twitter.com/labs/2/tweets/search?query=%s' %os.environ['query'],
        headers={'Authorization': 'Bearer %s' %token}
    )
    json_tweets = json.loads(tweets.data)
    ids = []
    for item in json_tweets['data']:
        ids.append(item['id'])
    
    return ids

def handler(event, context):
    sns_client = boto3.client('sns')
    ids = getTweets()
    sns_client.publish(
        TargetArn=os.environ['targetArn'],
        Message=json.dumps(ids) 
    )
    return {
        'statusCode': 200,
        'body': json.dumps(ids)
    }