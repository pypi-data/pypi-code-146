from functools import lru_cache
import boto3
import requests
import uuid
from spackle import log
from botocore.credentials import RefreshableCredentials
from boto3 import Session
from botocore.session import get_session


class DynamoDB:
    client = None
    identity_id = None
    table_name = None
    aws_region = None
    role_arn = None
    token = None

    def __init__(self):
        self.client = self._bootstrap_client()

    def get_item(self, key):
        return self.client.get_item(
            TableName=self.table_name,
            Key={
                "AccountId": {"S": self.identity_id},
                **key,
            },
        )

    def _bootstrap_client(self):
        log.log_debug("Bootstrapping DynamoDB client...")
        self._create_session()

        session_credentials = RefreshableCredentials.create_from_metadata(
            metadata=self._fetch_credentials(),
            refresh_using=self._fetch_credentials,
            method="sts-assume-role-with-web-identity",
        )
        session = get_session()
        session._credentials = session_credentials
        session.set_config_variable("region", self.aws_region)
        autorefresh_session = Session(botocore_session=session)
        return autorefresh_session.client("dynamodb", region_name=self.aws_region)

    def _create_session(self):
        from spackle import api_key, api_base

        session = requests.post(
            f"{api_base}/auth/session",
            headers={"Authorization": f"Bearer {api_key}"},
        ).json()
        self.identity_id = session["identity_id"]
        self.table_name = session["table_name"]
        self.aws_region = session["aws_region"]
        self.token = session["token"]
        self.role_arn = session["role_arn"]
        log.log_debug("Created session: %s" % session)

    def _fetch_credentials(self):
        log.log_debug("Refreshing credentials...")
        sts_client = boto3.client("sts")
        response = sts_client.assume_role_with_web_identity(
            RoleArn=self.role_arn,
            RoleSessionName=str(uuid.uuid4()),
            WebIdentityToken=self.token,
        )
        return {
            "access_key": response["Credentials"]["AccessKeyId"],
            "secret_key": response["Credentials"]["SecretAccessKey"],
            "token": response["Credentials"]["SessionToken"],
            "expiry_time": response["Credentials"]["Expiration"].isoformat(),
        }


@lru_cache(maxsize=1)
def get_client():
    log.log_debug("Creating DynamoDB client...")
    return DynamoDB()
