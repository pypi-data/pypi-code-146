import json
import base64
from typing import Dict, Optional
import boto3
from botocore.exceptions import ClientError


def get_secret(secret_name: str, region_name: str) -> Dict:
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        return json.loads(secret)


def get_parameter(name: str, region: Optional[str] = None) -> Optional[str]:
    """Retrieve secret from Parameter Store.

    :param name: Name of the parameter
    :param region: AWS region otherwise env AWS_DEFAULT_REGION
    :return: Value of parameter
    """
    if region:
        client = boto3.client("ssm", region_name=region)
    else:
        client = boto3.client("ssm")

    try:
        parameter = client.get_parameter(Name=name, WithDecryption=True)
    except ClientError as e:
        raise e
    return parameter.get('Parameter', {}).get('Value')
