import json
import os

from boto3 import client, resource, session
from requests_aws_sign import AWSV4Sign

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")


def get_signed_auth():
    """Returns a signed uri for calling endpoints with IAM authorization."""

    sess = session.Session()
    credentials = sess.get_credentials()
    service = "execute-api"

    return AWSV4Sign(credentials, AWS_REGION, service)


def get_ssm_parameter(name, encrypted=False):
    """Return a parameter value from the Systems Manger parameter store.

    :param name: The parameter name.
    :param encrypted: Flag indicating if the value is encrypted or not.
    """
    cli = client("ssm")
    param = cli.get_parameter(Name=name, WithDecryption=encrypted)

    return param["Parameter"]["Value"] if param else None


def put_ssm_parameter(name, value, param_type='String', overwrite=True):
    """Create or update a parameter from the Systems Manger parameter store.

    :param name: The parameter name.
    :param value: A value for the parameter.
    :param param_type: String | StringList | SecureString.
    :param overwrite: Overwrite an existing parameter. The default value is True.
    """
    cli = client("ssm")
    param = cli.put_parameter(Name=name, Value=value, Type=param_type, Overwrite=overwrite)

    return param["Version"] if param else None


def get_secret(name):
    """Return a secret value from Secrets Manger.

    :param name: The secret name.
    """

    sess = session.Session()

    client = sess.client(service_name="secretsmanager", region_name=AWS_REGION)

    secret = client.get_secret_value(SecretId=name)

    return secret["SecretString"]


def enqueue(queue_name, message):
    """Adds a new message to a SQS Queue.

    :param queue_name: The name of SQS Queue.
    :param message: The message to publish
    """

    sqs = resource("sqs", region_name=AWS_REGION)
    queue = sqs.get_queue_by_name(QueueName=queue_name)

    queue.send_message(MessageBody=json.dumps({"Message": json.dumps(message)}))


def get_url(bucket_name, object, expiration_in_seconds=300):
    """Return a presigned  url of a s3 object.

    :param bucket_name: The name of the bucket.
    :param object: The S3 complete object path.
    :param expiration_in_seconds: The period in seconds until url expiration.
    """

    s3_client = client("s3")

    response = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object},
        ExpiresIn=expiration_in_seconds,
    )

    return response