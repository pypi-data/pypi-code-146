"""Functionality to manipulate S3 events from EventBridge"""
import os
from typing import Any, Dict

from dai_python_commons.dai_error import MissingInputError, IncorrectInputValueError


class EventBridgeS3Event:
    """
    Class that provides useful functions to handle Event Bridge S3 events
    """

    @staticmethod
    def validate_config_dict(event_dict: Dict[str, Any]) -> None:
        """
        Validates that essential fields are present in an event bridge s3 event

        :param event_dict: The S3 EventBridge event given as a dictionary
        :return: Nothing, but it raises an exception if the event does not pass the validation
        """
        missing_fields = [field for field in ["source", "detail"] if field not in event_dict]
        if len(missing_fields) > 0:
            raise MissingInputError(missing_fields, "Incorrect event bridge s3 event, fields are missing.")

        # Make sure this is an s3 event
        if event_dict.get("source") != "aws.s3":
            raise IncorrectInputValueError({"source": event_dict["source"]}, "The source should be aws.s3")

        # check that the important fields are there
        missing_fields = [field for field in ["bucket", "object"] if field not in event_dict["detail"]]
        if len(missing_fields) > 0:
            raise MissingInputError(missing_fields, "Missing needed information in s3 event, detail field.")

        # check that the bucket name is present
        if "name" not in event_dict["detail"]["bucket"]:
            raise MissingInputError(["name"], "Missing 'name' field in detail.bucket")

        # check that the key is present
        if "key" not in event_dict["detail"]["object"]:
            raise MissingInputError(["key"], "Missing 'key' field in detail.object")

    def __init__(self, event_dict: Dict[str, Any]):
        """
        :param event_dict: The S3 EventBridge event given as a dictionary
        """
        EventBridgeS3Event.validate_config_dict(event_dict)

        self.s3_bucket = event_dict["detail"]["bucket"]["name"]
        self.s3_key = event_dict["detail"]["object"]["key"]
        self.s3_prefix = os.path.dirname(self.s3_key)
        self.original_event = event_dict

    def get_s3_path(self) -> str:
        """
        :return: Full s3 path for the object that generated the event
        """
        return f"s3://{self.s3_bucket}/{self.s3_key}"
