# pylint: disable=line-too-long,import-error,too-few-public-methods
"""
    CUSTOM WRITER CLASSES
        - Class which manages writer tasks like
        auth, write metadata, write file, create dir structure
"""
import json

import boto3


class GAV4Writer:
    """GAV4Writer Class"""

    def __init__(self, bucket, folder_path, profile_name=None):
        if profile_name is None:
            self.boto3_session = boto3.Session()
        else:
            self.boto3_session = boto3.Session(profile_name=profile_name)
        self.s3_resource = self.boto3_session.resource("s3")
        self.bucket = bucket
        self.folder_path = folder_path
        self.data = None

    def write_to_s3(self, payload):
        """
        This pulls the yielded dataset from the GA reader in a manner
        that consumes the dataset of the given view_id and date,
        and writes it to s3 so that duplication does not occur.
        :param payload: This is a key value object that looks like:
                        {
                            "data": list(),
                            "date": string,
                            "property_id": string
                        }
        """

        # confirm the payload keys are matching accurately with what is expected
        if list(payload.keys()).sort() != ["data", "date", "property_id"].sort():
            raise KeyError("Invalid payload")

        _property_id = payload["property_id"]
        _date = payload["date"].replace("-", "")
        _data = payload["data"]
        write_path = f"{self.folder_path}/{_property_id}/{_date}.json"
        if _data:
            print(
                f"Writing data to s3://{self.bucket}/{write_path} partitioned by property_id and date."
            )
            self.s3_resource.Object(self.bucket, write_path).put(Body=json.dumps(_data))
            self.data = {}
