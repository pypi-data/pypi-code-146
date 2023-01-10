import yaml
from typing import Optional


def yaml_to_dict(path: str):
    return yaml.safe_load(open(path))


def dict_to_yaml(path: str, values: dict, encoding: Optional[str] = None):
    with open(path, 'w', encoding=encoding) as f:
        yaml.dump(values, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
