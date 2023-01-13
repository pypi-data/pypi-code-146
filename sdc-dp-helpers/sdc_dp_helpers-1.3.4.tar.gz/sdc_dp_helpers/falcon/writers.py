# pylint: disable=too-few-public-methods

"""
    CUSTOM WRITER CLASSES
"""
import re
import json

# from datetime import datetime

import boto3


class CustomFalconWriter:
    """ "
    Writer for falcon API
    Works with dictionary object from the readers
    """

    def __init__(self, bucket, file_path, profile_name=None):
        if profile_name is None:
            self.boto3_session = boto3.Session()
        else:
            self.boto3_session = boto3.Session(profile_name=profile_name)
        self.s3_resource = self.boto3_session.resource("s3")
        self.bucket = bucket
        self.file_path = file_path
        self.success = False

    def is_success(self):
        """Updates the Write Sucsess to True"""
        self.success = True

    def write_to_s3(self, payload: dict) -> None:
        """
        This pulls the yielded dataset from the GA reader in a manner
        that consumes the dataset of the given view_id and date,
        and writes it to s3 so that duplication does not occur.
        :param payload: This is a key value object that looks like:
                        {
                            "data": list(),
                            "date": string,
                            "networks": string
                        }
        """

        # confirm the payload keys are matching accurately with what is expected
        if not {"data", "date", "networks"}.issubset(set(payload.keys())):
            raise KeyError("Invalid payload expecting: date, data, networks")

        if not re.search(r"\d{4}\-\d{2}\-\d{2}", payload["date"]):
            raise ValueError(
                "Invalid date format for partitioning expected: 'YYYY-mm-dd'"
            )

        if not isinstance(payload["data"], list):
            raise TypeError("Invalid data passed: expected List[Dict, Dict]")

        _data: list = payload["data"]
        _date: str = payload["date"].replace("-", "")
        _networks: str = payload["networks"]

        write_path: str = f"{self.file_path}/{_networks}/{_date}.json"
        if _data:
            print(
                f"Writing data to s3://{self.bucket}/{write_path}  \
                partitioned by networks and date."
            )
            self.s3_resource.Object(self.bucket, write_path).put(Body=json.dumps(_data))
            self.is_success()
