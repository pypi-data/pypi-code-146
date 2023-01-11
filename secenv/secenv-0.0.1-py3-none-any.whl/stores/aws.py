import boto3
import json
import os
from . import EnvPrefix, StoreInterface


class Store(StoreInterface):
    def __init__(self, name, infos):
        self.name = name

        region = super().get_from_config(name, "region", infos)
        key_id = super().get_from_config(name, "access_key_id", infos)
        secret_access_key = super().get_from_config(name, "secret_access_key", infos)

        client = boto3.client(
            "secretsmanager",
            region_name=region,
            aws_access_key_id=key_id,
            aws_secret_access_key=secret_access_key,
        )

        if "assume_role" in infos or f"{EnvPrefix}_{name}_assume_role" in os.environ:
            arn = infos.get("assume_role", os.getenv(f"{EnvPrefix}_{name}_assume_role"))
            role = client.assume_role(RoleArn=arn, RoleSessionName="MetastoreSession")
            creds = role["Credentials"]
            key_id = creds["AccessKeyId"]
            secret_access_key = creds["SecretAccessKey"]
            token = creds["SessionToken"]
            client = boto3.client(
                "secretsmanager",
                region_name=region,
                aws_access_key_id=key_id,
                aws_secret_access_key=secret_access_key,
                aws_session_token=token,
            )

        self.client = client

    def gen_parser(self, parser):
        parser.add_argument("secret")
        parser.add_argument("--key")

    def read_secret(self, secret, key="") -> str:
        search_result = self.client.list_secrets(
            MaxResults=2,
            Filters=[
                {"Key": "name", "Values": [secret]},
            ],
            SortOrder="asc",
        )
        if len(search_result["SecretList"]) == 0:
            raise Exception(f"Secret '{secret}' not found in store '{self.name}'")

        value = self.client.get_secret_value(
            SecretId=search_result["SecretList"][0]["ARN"],
        )

        if key:
            return json.loads(value["SecretString"])[key]
        else:
            return value["SecretString"]
