"""
A program that leverages AWS CDK to describe the structure, resources and
artifacts of the aws-wordcloud service. See examples in:
  https://github.com/aws-samples
  https://github.com/aws-samples/aws-cdk-examples
  https://github.com/search?q=org%3Aaws-samples%20CfnTable&type=codecdk

For the classes used throughout this program, see the AWS CDK Python reference
in:
  https://docs.aws.amazon.com/cdk/api/v2/python/
"""

from aws_cdk import Duration, Stack
from aws_cdk import aws_apigateway as aws_apigw
from aws_cdk import aws_lambda
from constructs import Construct


class AWSWordCloudStack(Stack):
    """
    This class defines the structure, resource and artifacts of the
    aws-wordcloud service through AWS CDK Constructs.
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Defines Lambda function to create word clouds
        create_wc_lambda = aws_lambda.Function(
            self,
            "CreateWordCloudFunction",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="handler.lambda_handler",
            code=aws_lambda.Code.from_asset(
                "lambda/create", exclude=["__pycache__", "*.pyc"]
            ),
            memory_size=350,
            timeout=Duration.seconds(180),  # Increases timeout (in seconds)
            # Sets environment variables
            environment={"MPLCONFIGDIR": "/tmp/matplotlib"},  # See issue #14
        )

        # Defines the API Gateway to trigger Lambda functions
        apigw = aws_apigw.RestApi(
            self,
            "WordCloudApi",
            rest_api_name="WordCloud Service",
            description="This service creates wordcloud images.",
        )

        create_wc_integration = aws_apigw.LambdaIntegration(create_wc_lambda)

        # the API will have the following endpoints:
        # POST /mindmap/create: Create a new mindmap from a JSON payload with the mindmap tree data

        wordcloud_resource = apigw.root.add_resource("wordcloud")
        create_path_resource = wordcloud_resource.add_resource("create")
        create_path_resource.add_method(
            "POST", create_wc_integration
        )  # POST /wordcloud/create
