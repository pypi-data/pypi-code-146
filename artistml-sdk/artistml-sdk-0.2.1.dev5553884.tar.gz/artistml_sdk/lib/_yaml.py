from typing import Any
from typing import Mapping

import yaml


def load_yaml(yaml_path: str) -> Mapping[str, Any]:
    with open(yaml_path, "r") as f:
        return yaml.safe_load(f)


def write_yaml(yaml_content, file_path: str):
    with open(file_path, "w") as f:
        f.write(yaml.safe_dump(yaml_content))
