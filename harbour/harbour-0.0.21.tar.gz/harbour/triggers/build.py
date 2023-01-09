import hashlib
import json
import urllib
import os

import boto3

from datetime import datetime

def handler(event, context):

    codebuild = boto3.client('codebuild')

    # Messages from SQS
    for message in event['Records']:

        body = json.loads(message['body'])

        # Messages from S3
        for record in body['Records']:

            key = urllib.parse.unquote(record['s3']['object']['key'])

            # Starts to build the image
            response = codebuild.start_build(
                projectName=os.getenv('BUILDER_PROJECT_NAME'),
                environmentVariablesOverride=[
                    {
                        'name': 'IMAGE_TAG',
                        'value': key.replace('build/artifacts/', ''),
                        'type': 'PLAINTEXT'
                    },
                ],
                sourceLocationOverride=f"{record['s3']['bucket']['name']}/{key}",
                idempotencyToken=record['s3']['object']['eTag']
            )
