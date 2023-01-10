import os
import boto3
import json
from botocore.exceptions import ClientError

class Tks3():
    def __init__(self, region=None):
        """
        :param region: The region for AWS S3
        """
        self.service_name = 's3'
        if region is None:
            region = os.getenv("S3_REGION")
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
        This method creates the boto3 client for AWS, The client can later be accessed using 'self.client'
        :return: Self object
        """
        if self.access_key is None or self.secret_key is None:
            self.client = boto3.client(service_name=self.service_name, region_name=self.region)
        else:
            self.client = boto3.client(service_name=self.service_name, region_name=self.region,
                                       aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        return self

    def get_resource(self):
        """
        This method creates the boto3 resource for AWS, The resource can later be accessed using 'self.resource'
        :return: Self object
        """
        if self.access_key is None or self.secret_key is None:
            self.resource = boto3.resource(service_name=self.service_name, region_name=self.region)
        else:
            self.resource = boto3.resource(service_name=self.service_name, region_name=self.region,
                                           aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        return self

    def generate_presigned_get_url(self, s3_bucket, s3_key):
        """
        :param s3_bucket: S3 Bucket where the file is present
        :param s3_key: S3 Key of the file
        :return: Signed Get URL to access the file.
        """
        self.get_client()
        url = self.client.generate_presigned_url('get_object', Params={'Bucket': s3_bucket, 'Key': s3_key}, ExpiresIn=3600)
        url = url.replace(f"s3.{self.region}.amazonaws.com/{s3_bucket}", f"{s3_bucket}.s3-{self.region}.amazonaws.com")
        return url

    def generate_presigned_post_url(self, s3_bucket, s3_key):
        """
        :param s3_bucket: S3 Bucket where the file will be uploaded
        :param s3_key: S3 Key of the file
        :return: Signed Post URL along with the credentials for uploading a file.
        """
        self.get_client()
        url = self.client.generate_presigned_post(s3_bucket, s3_key, ExpiresIn=3600)
        return url

    def get_file_content(self, s3_bucket, s3_key, encoding="utf-8"):
        """
        :param s3_bucket: S3 Bucket where the file is present
        :param s3_key: S3 Key of the file
        :return: File content decoded with utf-8 encoding present in s3
        """
        self.get_resource()
        obj = self.resource.Object(s3_bucket, s3_key)
        body = obj.get()['Body'].read().decode(encoding=encoding, errors="ignore")
        return body

    def get_file_object(self, s3_bucket, s3_key):
        """
        :param s3_bucket: S3 Bucket where the file is present
        :param s3_key: S3 Key of the file
        :return: File object without decoding or reading
        """
        self.get_resource()
        return self.resource.Object(s3_bucket, s3_key).get()

    def upload_local_file_to_s3(self, s3_bucket, s3_key, local_path):
        """
        :param s3_bucket: S3 Bucket where the file is present
        :param s3_key: S3 Key of the file
        :param local_path: Local path of the file object
        :return:
        """
        try:
            self.get_client()
            self.client.upload_file(local_path, s3_bucket, s3_key)
            return True
        except Exception as e:
            print("Exception at upload_local_file_to_s3", str(e))
            return False

    def list_objects(self, s3_bucket, s3_key="/"):
        """
        :param s3_bucket: S3 Bucket which is to be used
        :param s3_key: S3 Key which needs to be listed eg: / will list all the objects in the root of the bucket (default is for the root)
        :return: A List of keys for the objects under the provided key.
        """
        objects = []
        self.get_client()
        has_next = True
        next_token = None
        while has_next:
            if next_token is None:
                response = self.client.list_objects_v2(Bucket=s3_bucket, Prefix=s3_key)
            else:
                response = self.client.list_objects_v2(Bucket=s3_bucket, Prefix=s3_key, ContinuationToken=next_token)

            if response["IsTruncated"]:
                next_token = response["NextContinuationToken"]
            else:
                has_next = False
            if 'Contents' in response:
                objects.extend(response["Contents"])
        return objects

    def read_json_from_s3(self, s3_bucket, s3_key):
        """
        :param s3_bucket: S3 Bucket where the file is present
        :param s3_key: S3 Key of the file
        :return: the data in Json File - An Object that can be used directly
        """
        self.get_client()
        response = self.client.get_object(Bucket=s3_bucket, Key=s3_key)
        responseJson = json.loads(response['Body'].read().decode('utf-8'))
        return responseJson







