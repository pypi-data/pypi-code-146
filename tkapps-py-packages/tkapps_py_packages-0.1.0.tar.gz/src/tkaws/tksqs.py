import os
import boto3

class Tksqs():
    def __init__(self, region=None):
        """
        :param region: The region for AWS SQS
        """
        self.service_name = 'sqs'
        if region is None:
            region = os.getenv("SQS_REGION")
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
        To be used internally for the purpose of creating the boto3 client of sqs.
        This method creates the boto3 client for AWS, The client can later be accessed using 'self.client'
        :return: Self object (Tksqs Object)
        """
        if self.access_key is None or self.secret_key is None:
            self.client = boto3.client(service_name=self.service_name, region_name=self.region)
        else:
            self.client = boto3.client(service_name=self.service_name, region_name=self.region,
                                       aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        return self

    def get_resource(self):
        """
        To be used internally for the purpose of creating the boto3 resource of sqs.
        This method creates the boto3 resource for AWS, The resource can later be accessed using 'self.resource'
        :return: Self object (Tksqs Object)
        """
        if self.access_key is None or self.secret_key is None:
            self.resource = boto3.resource(service_name=self.service_name, region_name=self.region)
        else:
            self.resource = boto3.resource(service_name=self.service_name, region_name=self.region,
                                           aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        return self

    def get_all_queues(self):
        """
        :return: returns a list of all SQS Queues
        """
        self.get_resource()
        all_queues = self.resource.queues.all()
        return all_queues

    def send_by_queue_name(self, queue_name, message):
        """
        :param queue_name: Name of the Queue where the message will be sent
        :param message: message object to be sent.
        :return:
        """
        self.get_client()
        queue = self.client.get_queue_by_name(QueueName=queue_name)
        response = queue.send_message(MessageBody=str(message))
        return response


