from enum import Enum
import os

import yaml


class convert_struct:

    def __init__(self, **entries):
        for k, v in entries.items():
            setattr(self, k, v)


def load_yaml(yaml_filepath):
    with open(yaml_filepath, 'r') as stream:
        config = yaml.safe_load(stream)
    for k, v in config.items():
        if 'path' in k:
            config[k] = os.path.expandvars(v)
    return convert_struct(**config)
