import os
import boto3
from botocore.exceptions import ClientError

class Tkses():
    def __init__(self, region=None):
        """
        :param region: The region for AWS SES
        """
        self.service_name = 'ses'
        if region is None:
            region = os.getenv("SES_REGION")
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
        To be used internally for the purpose of creating the boto3 client of ses.
        This method creates the boto3 client for AWS, The client can later be accessed using 'self.client'
        :return: Self object (Tkses Object)
        """
        if self.access_key is None or self.secret_key is None:
            self.client = boto3.client(service_name=self.service_name, region_name=self.region)
        else:
            self.client = boto3.client(service_name=self.service_name, region_name=self.region,
                                       aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        return self

    def send_html_email(self, email_message):
        """
        :param email_message: email_message object (Note: This must be a Tkemail object)
        :return: Response of sending the email
        """
        try:
            self.get_client()
            destination = {'ToAddresses': email_message.to_emails, 'CcAddresses': email_message.cc_emails, 'BccAddresses': email_message.bcc_emails}
            response = self.client.send_email(
                Source=email_message.from_email,
                Destination=destination,
                Message={'Subject': {'Data': email_message.subject}, 'Body': {'Html': {'Data': email_message.message.as_string()}}}
            )
            return response
        except ClientError as e:
            print(e.response['Error']['Message'])
            return False


    def send_email(self, email_message):
        """
        :param email_message: email_message object (Note: This must be a Tkemail object)
        :return: Response of sending the email
        """
        try:
            self.get_client()
            response = self.client.send_raw_email(
                Source= email_message.from_email,
                Destinations=email_message.to_emails + email_message.cc_emails + email_message.bcc_emails,
                RawMessage={
                    'Data': email_message.message.as_string(),
                }
            )
            return response
        except ClientError as e:
            print(e.response['Error']['Message'])
            return False



