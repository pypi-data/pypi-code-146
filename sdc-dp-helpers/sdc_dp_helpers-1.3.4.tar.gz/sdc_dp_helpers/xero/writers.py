# pylint: disable=too-few-public-methods,unused-imports

"""
    CUSTOM WRITER CLASS FOR XERO DATA
"""
# import os
import json
import datetime
import boto3


class CustomS3JsonWriter:
    """Class to write files to s3"""

    def __init__(self, bucket: str, profile_name: str = None) -> None:
        self.bucket = bucket
        self.profile_name = profile_name
        self.data = {}

        if profile_name is None:
            self.boto3_session = boto3.Session()
        else:
            self.boto3_session = boto3.Session(profile_name=profile_name)

        self.s3_resource = self.boto3_session.resource("s3")

    def write_to_s3(self, json_data: dict, config: dict) -> None:
        """
        Construct partitioning and file name conventions in s3
        according to business specifications, and write to S3.
        """

        self.data = json_data
        if not json_data:
            return
        if not (
            config.get("data_variant")
            and config.get("collection_name")
            and config.get("tenant_name")
        ):
            raise ValueError(
                'Ensure config has keys "data_variant","collection_name", "tenant_name"'
            )
        data_variant = config["data_variant"].lower()
        collection_name = config["collection_name"].lower()
        organisation_name = config["tenant_name"].lower()
        _date = config.get(
            "date", config.get("date", datetime.datetime.now().strftime("%Y-%m-%d"))
        ).replace("-", "")

        key_path = f"{collection_name}/{data_variant}/{organisation_name}/{_date}.json"

        # in the case of reports we want to add contact_id as a partition_part,
        # let's check for extra partition_parts
        partition_part = config.get("partition_part")
        if partition_part:
            key_path = key_path.replace(
                f"{organisation_name}/", f"{organisation_name}/{partition_part}/"
            )

        # replace any '-' in the path, just in case; we don't want s3 to panic
        key_path = "_".join(key_path.split("-"))
        key_path = "_".join(key_path.split(" "))

        print(f"Write path: S3://{self.bucket}/{key_path}")
        self.s3_resource.Object(self.bucket, key_path).put(Body=json.dumps(json_data))
