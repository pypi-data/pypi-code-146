from typing import Union


from mypy_boto3_s3 import S3Client
from mypy_boto3_sqs import SQSClient

from ..aws_operations import (
    s3_put_object_bytes,
    sqs_send_message_fifo,
)
from ..custom_types import HttpError


def save_to_s3_and_send_sqs_update(
    s3_client: S3Client,
    s3_bucket: str,
    s3_key: str,
    s3_body_bytes: bytes,
    sqs_client: SQSClient,
    sqs_queue_url: str,
    sqs_message_body: str,
    sqs_message_group_id: str,
) -> Union[bool, HttpError]:

    s3_response = s3_put_object_bytes(
        s3_client=s3_client,
        s3_bucket=s3_bucket,
        s3_key=s3_key,
        s3_body_bytes=s3_body_bytes,
    )
    if isinstance(s3_response, HttpError):
        return s3_response

    sqs_message_sent = sqs_send_message_fifo(
        sqs_client=sqs_client,
        sqs_queue_url=sqs_queue_url,
        sqs_message_body=sqs_message_body,
        sqs_message_group_id=sqs_message_group_id,
    )
    if isinstance(sqs_message_sent, HttpError):
        return sqs_message_sent

    return True
