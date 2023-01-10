import os
import boto3
import json
from decimal import Decimal

class Tklambda():
    def __init__(self, region=None):
        """
        :param region: The region for AWS Lambda
        """
        self.service_name = 'lambda'
        if region is None:
            region = os.getenv("LAMBDA_REGION")
        if region is None:
            region = os.getenv("REGION")
        if region is None:
            raise ValueError("REGION is missing in both ENV Variable and constructor params.")
        self.region = region
        self.access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.http_timeout = 60

    def get_client(self):
        """
        To be used internally for the purpose of creating the boto3 client of lambda.
        This method creates the boto3 client for AWS, The client can later be accessed using 'self.client'
        :return: Self object
        """
        if self.access_key is None or self.secret_key is None:
            self.client = boto3.client(service_name=self.service_name, region_name=self.region)
        else:
            self.client = boto3.client(service_name=self.service_name, region_name=self.region,
                                       aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        return self

    def invoke_lambda(self, lambda_arn, payload):
        """
        :param lambda_arn: ARN of the lambda which will be invoked
        :param payload: Payload that will be sent while invoking lambda (This will go as event in the lambda handler)
        :return: Invoke Response
        """
        def default(obj):
            if isinstance(obj, Decimal):
                return str(obj)
        self.get_client()
        response = self.client.invoke(
            FunctionName=lambda_arn,
            InvocationType='Event',
            Payload=json.dumps(payload, default=default)
        )
        return response


