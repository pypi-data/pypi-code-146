import logging
import boto3
from django.conf import settings


def delete_object_from_s3(s3key: str) -> None:
    """
    Django storages is not deleting objects even when we the delete() on the file.
    """

    if settings.AWS_S3_REGION_NAME and settings.AWS_STORAGE_BUCKET_NAME:
        s3client = boto3.client("s3", region_name=settings.AWS_S3_REGION_NAME)
        s3client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3key)
    else:
        logging.warning(
            f"Unable to delete {s3key} from S3. Missing AWS_S3_REGION_NAME or AWS_STORAGE_BUCKET_NAME."
        )
