# pylint: disable=line-too-long,import-error,too-few-public-methods
"""
    CUSTOM WRITER CLASSES
        - Class which manages writer tasks like
        auth, write metadata, write file, create dir structure
"""
import re
import json
import boto3


class GoogleKnowledgeGraphWriter:
    """GoogleKnowledgeGraphReader Class"""

    def __init__(self, bucket, folder_path, profile_name=None):
        if profile_name is None:
            self.boto3_session = boto3.Session()
        else:
            self.boto3_session = boto3.Session(profile_name=profile_name)
        self.s3_resource = self.boto3_session.resource("s3")
        self.bucket: str = bucket
        self.folder_path: str = folder_path
        self.success = False

    def is_success(self) -> None:
        """Update Instance Success Status to True"""
        self.success = True

    def write_to_s3(self, payload):
        """
        This pulls the yielded dataset from the Google Knowledge Graph reader
        and writes it to s3 so that duplication does not occur.
        :param payload: This is a key value object that looks like:
                        {
                            "data": list[dict, dict],
                            "date": string
                        }
        """

        # confirm the payload keys are matching accurately with what is expected
        if not {"data", "date"}.issubset(set(payload.keys())):
            raise KeyError("Invalid payload ensure you have date and data as keys")

        if not re.search(r"\d{4}\-\d{2}\-\d{2}", payload["date"]):
            raise ValueError(
                "Invalid date format for partitioning expected: 'YYYY-mm-dd'"
            )

        if not isinstance(payload["data"], list):
            raise TypeError("Invalid data passed: expected List[Dict, Dict]")

        _date = payload["date"].replace("-", "")
        _data = payload["data"]
        write_path = f"{self.folder_path}/{_date}.json"
        if _data:
            print(
                f"Writing data to s3://{self.bucket}/{write_path} partitioned by date."
            )
            self.s3_resource.Object(self.bucket, write_path).put(Body=json.dumps(_data))
            # this helps with unittesting so we set success to True
            self.is_success()
