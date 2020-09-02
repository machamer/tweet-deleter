from aws_cdk import (
    aws_iam as iam,
    aws_sns as sns,
    aws_lambda as _lambda,
    aws_events as events,
    aws_lambda_event_sources as event_sources,
    aws_events_targets as targets,
    core
)

class CdktweetsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        topic = sns.Topic(self, 'tweets', display_name='tweets')

        get_tweets_lambda = _lambda.Function(
            self, 'GetTweets',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda/get_tweets'),
            handler='get_tweets.handler',
            environment={
                'consumerKey': 'consumerKey', 
                'consumerSecret': 'consumerSecret',
                'query': 'query',
                'targetArn': topic.topic_arn}
        )
        topic.grant_publish(get_tweets_lambda)
    
        delete_tweets_lambda = _lambda.Function(
            self, 'DeleteTweets',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda/delete_tweets'),
            handler='delete_tweets.handler',
            environment={
                'consumerKey': 'consumerKey', 
                'consumerSecret': 'consumerSecret',
                'accessTokenKey': 'accessTokenKey',
                'accessTokenSecret': 'accessTokenSecret'}
        )
        rule = events.Rule(
            self, 
            'get_tweets_weekly', 
            schedule=events.Schedule.cron(
                minute='0',
                hour='0',
                month='*',
                year='*',
                week_day='SUN'
            ), 
        )
        rule.add_target(targets.LambdaFunction(get_tweets_lambda))

        sns_eventsource = event_sources.SnsEventSource(topic)
        delete_tweets_lambda.add_event_source(sns_eventsource)
      