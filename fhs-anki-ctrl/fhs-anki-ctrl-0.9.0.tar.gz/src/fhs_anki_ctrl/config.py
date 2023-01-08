"""Load config."""

import os
import sys
import yaml

from .__version__ import __project_name__


def get_default_config():
    """Get default config.

    Returns:
        config
    """
    return {'host': 'http://localhost:8765'}


def config_read(config=""):
    """Load config from disk.

    Args:
        config: config path to load.

    Returns:
        config
    """
    if config is None or config == "":
        config = f"~/.{__project_name__}.yaml"

    try:
        with open(os.path.expanduser(config), "r") as file:
            config_dict = yaml.load(file, Loader=yaml.FullLoader)
    except Exception:  # noqa:B902
        print("using default config....")
        return get_default_config()
    return config_dict

