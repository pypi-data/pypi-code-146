import boto3
from botocore.exceptions import ClientError

from gdshoplib.core.settings import S3Settings


class S3:
    def __init__(self, data):
        self.data = data
        self.content = None
        self.s3_settings = S3Settings()
        self.__session = None
        self.__client = None

    @property
    def session(self):
        if not self.__session:
            self.__session = boto3.session.Session()

        return self.__session

    @property
    def s3(self):
        if not self.__client:
            self.__client = self.session.client(
                service_name="s3",
                endpoint_url=self.s3_settings.ENDPOINT_URL,
                aws_access_key_id=self.s3_settings.ACCESS_KEY,
                aws_secret_access_key=self.s3_settings.SECRET_KEY,
            )
        return self.__client

    def put(self):
        return self.s3.put_object(
            Bucket=self.s3_settings.BUCKET_NAME,
            Key=self.data.file_key,
            Body=self.data.content,
            ACL="public-read",
            StorageClass="COLD",
            ContentType=self.data.mime,
        )

    def exists(self):
        try:
            self.s3.head_object(
                Bucket=self.s3_settings.BUCKET_NAME, Key=self.data.file_key
            )
        except ClientError:
            return False
        else:
            return True

    def get(self):
        try:
            return self.s3.get_object(
                Bucket=self.s3_settings.BUCKET_NAME, Key=self.data.file_key
            )
        except ClientError as ex:
            if ex.response["Error"]["Code"] == "NoSuchKey":
                return None
            raise ex

    def delete(self):
        return self.s3.delete_object(
            Bucket=self.s3_settings.BUCKET_NAME, Key=self.data.file_key
        )
