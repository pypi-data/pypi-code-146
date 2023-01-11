import json
import os

from google.protobuf.json_format import ParseDict
import yaml

import truera.client.client_utils as client_utils


def load_dict_from_file(file):
    _, ext = os.path.splitext(file)

    if ext == ".yml" or ext == ".yaml":
        with open(file) as fp:
            return yaml.safe_load(fp)
    elif ext == ".json":
        with open(file) as fp:
            return json.load(fp)
    else:
        message = (
            "Could not determine type of provided file. Please "
            "provide a '.json', '.yaml', or '.yml' file. Provided "
            "file: " + file
        )
        raise client_utils.NotSupportedFileTypeException(message)


def parse_message_from_file(file, pb_instance):
    json_dict = load_dict_from_file(file)
    ParseDict(json_dict, pb_instance)
    return
