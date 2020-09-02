#!/usr/bin/env python3

from aws_cdk import core

from cdktweets.cdktweets_stack import CdktweetsStack


app = core.App()
CdktweetsStack(app, "cdktweets", env={'region': 'us-east-1'})

app.synth()
