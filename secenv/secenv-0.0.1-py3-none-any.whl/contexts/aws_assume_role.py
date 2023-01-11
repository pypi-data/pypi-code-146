import boto3


def aws_assume_role(access_key_id, secret_access_key, role_arn):
    session = boto3.Session(
        aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key
    )

    sts_client = session.client("sts")
    assumed_role_object = sts_client.assume_role(
        RoleArn=role_arn, RoleSessionName="AssumeRoleSession1"
    )

    credentials = assumed_role_object["Credentials"]
    access_key_id = credentials["AccessKeyId"]
    secret_access_key = credentials["SecretAccessKey"]
    session_token = credentials["SessionToken"]

    return access_key_id, secret_access_key, session_token
