import json
import boto3


def get_secret(secret_id):
    client = boto3.client('secretsmanager')
    secret = client.get_secret_value(SecretId=secret_id)
    return json.loads(secret['SecretString'])


def update_secret(
        secret_id,
        access_token,
        refresh_token,
        access_expiry
):
    client = boto3.client('secretsmanager')
    value = json.dumps({
        'access_token': access_token,
        'access_expiry': access_expiry,
        'refresh_token': refresh_token,
    })
    client.update_secret(
        SecretId=secret_id,
        SecretString=value,
    )
