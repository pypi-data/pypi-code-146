import os
import boto3
from botocore.exceptions import ClientError

class Tksns():
    def __init__(self, region=None):
        """
        :param region: The region for AWS SES
        """
        self.service_name = 'sns'
        if region is None:
            region = os.getenv("SES_REGION")
        if region is None:
            region = os.getenv("REGION")
        if region is None:
            raise ValueError("REGION is missing in both ENV Variable and constructor params.")
        self.region = region
        self.client = boto3.client(service_name=self.service_name, region_name=self.region)
        self.http_timeout = 60



