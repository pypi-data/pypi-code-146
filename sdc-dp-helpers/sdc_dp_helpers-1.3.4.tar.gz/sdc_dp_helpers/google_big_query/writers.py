# pylint: disable=too-few-public-methods
# pylint: disable=no-member

"""
    CUSTOM WRITER CLASSES
"""
import json

import boto3


class CustomS3JsonWriter:
    """Class Extends Basic LocalGZJsonWriter"""

    def __init__(self, bucket, file_path, profile_name=None):
        self.bucket = bucket
        self.file_path = file_path
        self.profile_name = profile_name

        if profile_name is None:
            self.boto3_session = boto3.Session()
        else:
            self.boto3_session = boto3.Session(profile_name=profile_name)
        self.s3_resource = self.boto3_session.resource("s3")

    def write_partition_to_s3(self, json_data):
        """
        Partitions data by date to reduce duplication in s3.
        So the plan is to ensure that if we:
            - pull from a specific date, we overwrite all that days data in the buckets.
            - this way, we ensure all data is original and in its most updated state.
        """
        # dimension = json_data["dimension"]
        date = json_data["date"].replace("-", "")
        dataset = json_data["data"]
        business = json_data["business"]
        key_path = f"{self.file_path}/{business}/{date}.json"
        print(f"Writing data to {key_path}.")
        self.s3_resource.Object(self.bucket, key_path).put(Body=json.dumps(dataset))
