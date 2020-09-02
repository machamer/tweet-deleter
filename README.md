This application uses the AWS CDK to define and deploy the AWS resources to interact with the necessary Twitter APIs to regularly delete a user's tweets on a defined schedule.


### How to Run
1. Create a Twitter [Developer Account](https://developer.twitter.com/en/apply)
2. Create a Twitter [App](https://developer.twitter.com/en/apps/create)
3. Get Started with [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/work-with-cdk-python.html)
4. Set [environment variables](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html) for `accessTokenKey`, `accessTokenSecret`, `consumerKey`, `consumerSecret` and `query`
5. Define the deletion schedule by setting the Cron expression for the `rule`.  Due to limitations of the Twitter API, it cannot be greater than 7 days.  
6. `cdk synth`
7. `cdk deploy`