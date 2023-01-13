from typing import List, Union

from botocore.response import StreamingBody
from mypy_boto3_s3 import S3Client
from mypy_boto3_s3.type_defs import (
    DeleteObjectOutputTypeDef,
    GetObjectOutputTypeDef,
    PutObjectOutputTypeDef,
)
from mypy_boto3_secretsmanager import SecretsManagerClient
from mypy_boto3_secretsmanager.type_defs import GetSecretValueResponseTypeDef
from mypy_boto3_ses import SESClient
from mypy_boto3_ses.type_defs import SendEmailResponseTypeDef
from mypy_boto3_sqs import SQSClient
from mypy_boto3_sqs.type_defs import SendMessageResultTypeDef
from pydantic import EmailStr

from ..custom_types import HttpError
from ..http_return import http_error

#
# SecretsManager
#


e: List[str] = [
    "ClientError",
    "DecryptionFailure",
    "EncryptionFailure",
    "InternalServiceError",
    "InvalidNextTokenException",
    "InvalidParameterException",
    "InvalidRequestException",
    "LimitExceededException",
    "MalformedPolicyDocumentException",
    "PreconditionNotMetException",
    "PublicPolicyException",
    "ResourceExistsException",
    "ResourceNotFoundException",
]


def get_secret_string(
    secrets_manager_client: SecretsManagerClient, secret_id: str
) -> Union[str, HttpError]:
    try:
        secret_response: GetSecretValueResponseTypeDef = (
            secrets_manager_client.get_secret_value(SecretId=secret_id)
        )
        return secret_response.get(
            "SecretString",
            default=http_error(
                404,
                "SecretsManager Error",
                [
                    (
                        f"Could not get secret {secret_id} becasue GetSecretValueResponse does not have a SecretString field."
                        f"The secret might be binary instead of string."
                    )
                ],
            ),
        )

    except secrets_manager_client.exceptions.ClientError as ce:
        status_code = ce.response.get("ResponseMetadata", {}).get("HTTPStatusCode", 500)
        error_code = ce.response.get("Error", {}).get("Code", "ErrorCodeMissing")
        return http_error(
            status_code,
            "SecretsManager Error",
            [
                f"Could not get {secret_id} and a ClientError happened with status code: {status_code}",
                error_code,
            ],
        )

    except Exception as ex:
        return http_error(
            500,
            "SecretsManager Error",
            [f"Could not get {secret_id} and an exception happened: {ex}"],
        )


def get_secret_binary(
    secrets_manager_client: SecretsManagerClient, secret_id: str
) -> Union[bytes, HttpError]:
    try:
        secret_response: GetSecretValueResponseTypeDef = (
            secrets_manager_client.get_secret_value(SecretId=secret_id)
        )
        return secret_response.get(
            "SecretBinary",
            http_error(
                status_code=404,
                message="SecretsManager Error",
                reasons=[
                    (
                        f"Could not get secret {secret_id} becasue GetSecretValueResponse does not have a SecretString field."
                        f"The secret might be string instead of binary."
                    )
                ],
            ),
        )

    except secrets_manager_client.exceptions.ClientError as ce:
        status_code = ce.response.get("ResponseMetadata", {}).get("HTTPStatusCode", 500)
        error_code = ce.response.get("Error", {}).get("Code", "ErrorCodeMissing")
        return http_error(
            status_code,
            "SecretsManager Error",
            reasons=[
                f"Could not get {secret_id} and a ClientError happened with status code: {status_code}",
                error_code,
            ],
        )

    except Exception as ex:
        return http_error(
            500,
            "SecretsManager Error",
            [f"Could not get {secret_id} and an exception happened: {ex}"],
        )


#
# S3
#


e = [
    "BucketAlreadyExists",
    "BucketAlreadyOwnedByYou",
    "ClientError",
    "InvalidObjectState",
    "NoSuchBucket",
    "NoSuchKey",
    "NoSuchUpload",
    "ObjectAlreadyInActiveTierError",
    "ObjectNotInActiveTierError",
]


def s3_get_object_stream(
    s3_client: S3Client, s3_bucket: str, s3_key: str
) -> Union[StreamingBody, HttpError]:
    try:
        s3_response: GetObjectOutputTypeDef = s3_client.get_object(
            Bucket=s3_bucket, Key=s3_key
        )
        s3_stream_maybe = s3_response.get("Body")

        if s3_stream_maybe is None:
            return http_error(
                500, "S3 Error", [f"Could not get Body field from s3 response"]
            )

        s3_stream_maybe.set_socket_timeout(3)
        return s3_stream_maybe

    except (s3_client.exceptions.NoSuchKey, s3_client.exceptions.NoSuchBucket) as ce:
        error_code = ce.response.get("Error", {}).get("Code", "ErrorCodeMissing")
        return http_error(
            404, "S3 Error", [f"Could not get s3://{s3_bucket}/{s3_key}", error_code]
        )

    except s3_client.exceptions.ClientError as ce:
        status_code = ce.response.get("ResponseMetadata", {}).get("HTTPStatusCode", 500)
        error_code = ce.response.get("Error", {}).get("Code", "ErrorCodeMissing")
        return http_error(
            status_code=status_code,
            message="S3 Error",
            reasons=[
                f"Could not get s3://{s3_bucket}/{s3_key} and a ClientError happened with status code: {status_code}",
                error_code,
            ],
        )

    except Exception as ex:
        return http_error(
            500,
            "S3 Error",
            [f"Could not get s3://{s3_bucket}/{s3_key} and a Exception happened: {ex}"],
        )


def s3_get_object_bytes(
    s3_client: S3Client, s3_bucket: str, s3_key: str
) -> Union[bytes, HttpError]:
    try:

        s3_stream_maybe = s3_get_object_stream(
            s3_client=s3_client, s3_bucket=s3_bucket, s3_key=s3_key
        )
        if isinstance(s3_stream_maybe, HttpError):
            return s3_stream_maybe

        return s3_stream_maybe.read()

    except Exception as ex:
        return http_error(
            status_code=500,
            message="S3 Error",
            reasons=[
                f"Could not get key s3://{s3_bucket}/{s3_key} and a Exception happened: {ex}"
            ],
        )


def s3_put_object_bytes(
    s3_client: S3Client, s3_bucket: str, s3_key: str, s3_body_bytes: bytes
) -> Union[PutObjectOutputTypeDef, HttpError]:
    try:
        s3_response: PutObjectOutputTypeDef = s3_client.put_object(
            Bucket=s3_bucket, Key=s3_key, Body=s3_body_bytes
        )

        return s3_response

    except s3_client.exceptions.NoSuchBucket:
        return http_error(404, "S3 Error", [f"Could not find bucket: {s3_bucket}"])

    except s3_client.exceptions.ClientError as ce:
        status_code = ce.response.get("ResponseMetadata", {}).get("HTTPStatusCode", 500)
        error_code = ce.response.get("Error", {}).get("Code", "ErrorCodeMissing")
        return http_error(
            status_code=status_code,
            message="S3 Error",
            reasons=[
                f"Could not put key s3://{s3_bucket}/{s3_key} and a ClientError happened with status code: {status_code}",
                error_code,
            ],
        )

    except Exception as ex:
        return http_error(
            status_code=500,
            message="S3 Error",
            reasons=[
                f"Could not put key s3://{s3_bucket}/{s3_key} and a Exception happened: {ex}"
            ],
        )


def s3_delete_object(
    s3_client: S3Client, s3_bucket: str, s3_key: str
) -> Union[DeleteObjectOutputTypeDef, HttpError]:
    try:
        s3_response: DeleteObjectOutputTypeDef = s3_client.delete_object(
            Bucket=s3_bucket, Key=s3_key
        )

        return s3_response

    except s3_client.exceptions.ClientError as ce:
        status_code = ce.response.get("ResponseMetadata", {}).get("HTTPStatusCode", 500)
        error_code = ce.response.get("Error", {}).get("Code", "ErrorCodeMissing")
        return http_error(
            status_code=status_code,
            message="S3 Error",
            reasons=[
                f"Could not delete s3://{s3_bucket}/{s3_key} and a ClientError happened with status code: {status_code}",
                error_code,
            ],
        )


e = [
    "BatchEntryIdsNotDistinct",
    "BatchRequestTooLong",
    "ClientError",
    "EmptyBatchRequest",
    "InvalidAttributeName",
    "InvalidBatchEntryId",
    "InvalidIdFormat",
    "InvalidMessageContents",
    "MessageNotInflight",
    "OverLimit",
    "PurgeQueueInProgress",
    "QueueDeletedRecently",
    "QueueDoesNotExist",
    "QueueNameExists",
    "ReceiptHandleIsInvalid",
    "TooManyEntriesInBatchRequest",
    "UnsupportedOperation",
]


def sqs_send_message_fifo(
    sqs_client: SQSClient,
    sqs_queue_url: str,
    sqs_message_body: str,
    sqs_message_group_id: str,
) -> Union[SendMessageResultTypeDef, HttpError]:
    try:
        return sqs_client.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody=sqs_message_body,
            MessageGroupId=sqs_message_group_id,
        )
    except sqs_client.exceptions.ClientError as ce:
        status_code = ce.response.get("ResponseMetadata", {}).get("HTTPStatusCode", 500)
        error_code = ce.response.get("Error", {}).get("Code", "ErrorCodeMissing")
        return http_error(
            status_code,
            "SQS Error",
            [f"Could not send message to queue: {sqs_queue_url}", error_code],
        )
    except Exception as ex:
        return http_error(
            500,
            message="SQS Error",
            reasons=(
                f"Could not send SQS message {sqs_message_body} to queue_url: {sqs_queue_url}"
                f"message_group_id: {sqs_message_group_id} becasue of {ex}"
            ),
        )


e = [
    "AccountSendingPausedException",
    "AlreadyExistsException",
    "CannotDeleteException",
    "ClientError",
    "ConfigurationSetAlreadyExistsException",
    "ConfigurationSetDoesNotExistException",
    "ConfigurationSetSendingPausedException",
    "CustomVerificationEmailInvalidContentException",
    "CustomVerificationEmailTemplateAlreadyExistsException",
    "CustomVerificationEmailTemplateDoesNotExistException",
    "EventDestinationAlreadyExistsException",
    "EventDestinationDoesNotExistException",
    "FromEmailAddressNotVerifiedException",
    "InvalidCloudWatchDestinationException",
    "InvalidConfigurationSetException",
    "InvalidDeliveryOptionsException",
    "InvalidFirehoseDestinationException",
    "InvalidLambdaFunctionException",
    "InvalidPolicyException",
    "InvalidRenderingParameterException",
    "InvalidS3ConfigurationException",
    "InvalidSNSDestinationException",
    "InvalidSnsTopicException",
    "InvalidTemplateException",
    "InvalidTrackingOptionsException",
    "LimitExceededException",
    "MailFromDomainNotVerifiedException",
    "MessageRejected",
    "MissingRenderingAttributeException",
    "ProductionAccessNotGrantedException",
    "RuleDoesNotExistException",
    "RuleSetDoesNotExistException",
    "TemplateDoesNotExistException",
    "TrackingOptionsAlreadyExistsException",
    "TrackingOptionsDoesNotExistException",
]


def ses_send_email(
    ses_client: SESClient,
    ses_from_email: EmailStr,
    ses_to_emails: List[EmailStr],
    ses_email_subject: str,
    ses_email_body: str,
) -> Union[SendEmailResponseTypeDef, HttpError]:

    try:
        return ses_client.send_email(
            Destination={"ToAddresses": ses_to_emails},
            Message={
                "Body": {
                    "Html": {
                        "Charset": "utf-8",
                        "Data": ses_email_body,
                    },
                },
                "Subject": {
                    "Charset": "utf-8",
                    "Data": ses_email_subject,
                },
            },
            Source=ses_from_email,
        )
    except ses_client.exceptions.ClientError as ce:
        status_code = ce.response.get("ResponseMetadata", {}).get("HTTPStatusCode", 500)
        error_code = ce.response.get("Error", {}).get("Code", "ErrorCodeMissing")
        return http_error(
            status_code,
            "SES Error",
            [
                f"Could not send SES email message from: {ses_from_email} to: {ses_to_emails}",
                error_code,
            ],
        )
    except Exception as ex:
        return http_error(
            status_int=500,
            message="SES Error",
            reasons=(
                f"Could not send SES email message from: {ses_from_email} to: {ses_to_emails}"
                f"becasue of {ex}"
            ),
        )


# import boto3

# sqs = boto3.client("sqs")
# [e for e in dir(sqs.exceptions) if e[0].isupper()]

# s3 = boto3.client("s3")
# [e for e in dir(s3.exceptions) if e[0].isupper()]
