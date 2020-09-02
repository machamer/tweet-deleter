import json
import pytest

from aws_cdk import core
from cdktweets.cdktweets_stack import CdktweetsStack


def get_template():
    app = core.App()
    CdktweetsStack(app, "cdktweets")
    return json.dumps(app.synth().get_stack("cdktweets").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
