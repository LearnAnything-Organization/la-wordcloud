"""
FIXME Document this
"""

import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest
from handler import WordCloudHandler

from aws_wordcloud.aws_wordcloud_stack import AWSWordCloudStack


# example tests. To run these tests, uncomment this file along with the example
# resource in aws_wordcloud/aws_wordcloud_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AWSWordCloudStack(app, "aws-wordcloud")
    template = assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })


def test_wordcloud_generation():
    """
    Tests whether the generation of a word cloud returns a valid HTTP status
    code.
    """

    print("Testing word cloud generation")
    handler = WordCloudHandler()
    event = ' { "text": "This is a word cloud test" } '
    context = ""
    handler_result = handler(event, context)
    assert handler_result.get("statusCode") == 200  # HTTP OK


if __name__ == "__main__":
    pytest.main()
