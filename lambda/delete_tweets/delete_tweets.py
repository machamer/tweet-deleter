import os
import sys
import time
import json
import boto3
import urllib3
import twitter

def delete(ids):
    api = twitter.Api(consumer_key=os.environ['consumerKey'],
                        consumer_secret=os.environ['consumerSecret'],
                        access_token_key=os.environ['accessTokenKey'],
                        access_token_secret=os.environ['accessTokenSecret'])
    destroyer = TweetDestroyer(api)  

    count = 0
    for i in range(len(ids)):
        destroyer.destroy(ids[i])
        count += 1

    return count

class TweetDestroyer(object):
    def __init__(self, twitter_api):
        self.twitter_api = twitter_api

    def destroy(self, tweet_id):
        try:
            print("delete tweet %s" % tweet_id)
            self.twitter_api.DestroyStatus(tweet_id)
        except twitter.TwitterError as err:
            print("Exception: %s\n" % err.message)

def handler(event, context):
    print(event)
    count = delete(json.loads(event['Records'][0]['Sns']['Message']))
    return {
        'statusCode': 200,
        'body': json.dumps('Deleted %s tweets' %count )
    }