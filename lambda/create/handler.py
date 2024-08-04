"""
This module is responsible for generating wordcloud images.
"""

import os
import sys

# Adds lambda/packages to the system path.
# This must be done before importing any modules from the packages directory.
sys.path.append(os.path.join(os.path.dirname(__file__), "packages"))

import base64

from app_common.base_lambda_handler import BaseLambdaHandler
from app_common.app_utils import log_object
from wordcloud import WordCloud


class WordCloudHandler(BaseLambdaHandler):
    """
    This class is responsible for generating wordcloud images.
    """

    def generate_wordcloud(self, object_name, text: str = "Word1 Word2 Word3"):
        """
        Generate a wordcloud image.
        """
        full_local_path = BaseLambdaHandler.get_temp_dir_path() + object_name

        wc = WordCloud(
            width=400,
            height=300,
            background_color="white",
            repeat=False,
            margin=2,
            max_words=100,
        )
        wc.generate(text)
        wc.to_file(full_local_path)
        # return wc.to_image()
        return (wc, full_local_path)

    def handle(self):
        """
        Given a text, generates a wordcloud image of it.
        """

        # Generates the wordcloud image and reads the contents of the resulting
        # file
        object_name = self.body.get("object_name", "wordcloud.jpg")
        text = self.body.get("text", "Word1 Word2 Word3")
        (wc, wc_path) = self.generate_wordcloud(object_name, text)

        with open(wc_path, mode="rb") as wc_file:
            wc_bytes = wc_file.read()

        # Encodes the image in base64
        image_base64 = base64.b64encode(wc_bytes).decode("utf-8")

        # Returns the generated wordcloud image
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "image/png",
                "Content-Disposition": 'inline; filename="wordcloud.png"',
                "Content-Transfer-Encoding": "base64",
            },
            "body": image_base64,
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
