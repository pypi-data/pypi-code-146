from typing import Type

import google
from google.protobuf import json_format

from ._yaml import load_yaml
from ._yaml import write_yaml


def read_message(
    yaml_path: str, message_type: Type[google.protobuf.message.Message]
) -> google.protobuf.message.Message:
    return json_format.ParseDict(load_yaml(yaml_path), message_type())


def write_message(message: google.protobuf.message.Message, yaml_path: str):
    write_yaml(
        json_format.MessageToDict(message, preserving_proto_field_name=True),
        yaml_path)


def convert_message(
    src_message: google.protobuf.message.Message,
    tar_type: Type[google.protobuf.message.Message]
) -> google.protobuf.message.Message:
    return json_format.ParseDict(
        json_format.MessageToDict(src_message,
                                  preserving_proto_field_name=True),
        tar_type())
