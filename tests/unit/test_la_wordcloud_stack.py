import aws_cdk as core
import aws_cdk.assertions as assertions

from la_wordcloud.la_wordcloud_stack import LAWordCloudStack

# example tests. To run these tests, uncomment this file along with the example
# resource in la_wordcloud/la_wordcloud_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = LAWordCloudStack(app, "la-wordcloud")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
