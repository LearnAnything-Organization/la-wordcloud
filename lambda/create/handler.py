"""
This module is responsible for generating wordcloud images.
"""

import os
import sys

# Adds lambda/packages to the system path.
# This must be done before importing any modules from the packages directory.
sys.path.append(os.path.join(os.path.dirname(__file__), "packages"))

import base64
from io import BytesIO

from app_common.app_utils import log_object
from app_common.base_lambda_handler import BaseLambdaHandler
from wordcloud import WordCloud


class WordCloudHandler(BaseLambdaHandler):
    """
    This class is responsible for generating wordcloud images.
    """

    def generate_wordcloud(self, text: str):
        """
        Generates a wordcloud image.
        """

        wc = WordCloud(
            width=400,
            height=300,
            background_color="white",
            repeat=False,
            margin=2,
            max_words=100,
        )
        wc.generate(text)
        img = wc.to_image()

        return (wc, img)

    def handle(self):
        """
        Given a text, generates a wordcloud image of it.
        """

        # Generates the wordcloud image, saves its contents to a memory buffer
        # in PNG format and finally encodes the PNG content in base64
        text = self.body.get("text", "Word1 Word2 Word3")
        (wc, img) = self.generate_wordcloud(text)

        bio = BytesIO()
        img.save(bio, format="png")

        img_base64 = base64.b64encode(bio.getvalue()).decode("utf-8")

        # Returns the generated wordcloud image
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "image/png",
                "Content-Disposition": 'inline; filename="wordcloud.png"',
                "Content-Transfer-Encoding": "base64",
            },
            "body": img_base64,
            "isBase64Encoded": True,
        }


def lambda_handler(event, context):
    """
    This method handles lambda function invocations coming from AWS. Please
    refer to the ``aws_wordcloud_stack.py`` module to find out more about the
    configuration of the associated lambda function.
    """

    handler = WordCloudHandler()
    # Implicitly invokes __call__() ...
    #   ... which invokes _do_the_job() ...
    #     ... which invokes before_handle(), handle() and after_handle()
    return handler(event, context)
