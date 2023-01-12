import boto3
from django.conf import settings


s3client = boto3.client(
    "s3",
    region_name=settings.AWS_S3_REGION_NAME,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


def delete_object_from_s3(s3key: str) -> None:
    """
    Django storages is not deleting objects even when we the delete() on the file.
    """

    if settings.AWS_STORAGE_BUCKET_NAME:
        s3client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3key)
