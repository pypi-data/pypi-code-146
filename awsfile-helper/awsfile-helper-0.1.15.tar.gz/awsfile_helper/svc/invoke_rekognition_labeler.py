# -*- coding: utf-8 -*-
""" Invoke the Rekognition Labeler API """


import os
from typing import List
from boto3.resources.factory import ServiceResource

from baseblock import FileIO
from baseblock import BaseObject


class InvokeRekognitionLabeler(BaseObject):
    """ Invoke the Rekognition Labeler API """

    def __init__(self,
                 s3_client: ServiceResource):
        """ Change Log

        Created:
            13-Jan-2023
            craigtrim@gmail.com
            *   https://github.com/craigtrim/awsfile-helper/issues/7

        Args:
            s3 (ServiceResource): an activated s3 resource
        """
        BaseObject.__init__(self, __name__)
        self._s3_client = s3_client

    def process(self,
                input_directory: str,
                output_directory: str) -> None:
        """ Entry Point

        Args:
            input_directory (List[str]): a list of fully qualified file paths
            output_directory (List[str]): the output directory for the results
        """

        file_paths = FileIO.load_files(input_directory, 'jpg')

        for file_path in file_paths:

            with open(file_path, 'rb') as image:

                output_file_name = os.path.basename(
                    file_path).replace('.jpg', '.json')

                output_file_path = FileIO.join(
                    output_directory, output_file_name)

                if FileIO.exists(output_file_path):
                    continue

                try:

                    imgb = bytearray(image.read())
                    response = self._s3_client.detect_labels(
                        Image={'Bytes': imgb}, MaxLabels=10)

                    FileIO.write_json(response, output_file_path)

                except Exception as e:
                    self.logger.error('\n'.join([
                        'AWS Rekognition Error',
                        f'\tInput File: {file_path}',
                        f'\tError: {e}']))

                    text_file = os.path.basename(
                        file_path).replace('.jpg', '.txt')

                    FileIO.write_string(str(e), FileIO.join(
                        output_directory, text_file))
