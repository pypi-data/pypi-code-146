"""Huawei obs function."""
import tomllib


def obs_config(filepath):
    """Read obs config from toml file.

    Args:
        filepath (str): toml config file path.
    Returns:
        (str, str, str, str): access_id, secret_key, endpoint, bucket.
    """
    with open(filepath, "rb") as f:
        config = tomllib.load(f)

        access_key_id = config["obs"]["access_key_id"]
        secret_access_key = config["obs"]["secret_access_key"]
        endpoint = config["obs"]["endpoint"]
        bucket = config["obs"]["bucket"]
        return access_key_id, secret_access_key, endpoint, bucket


def server_config(filepath):
    """Read server config from toml file.

    Args:
        filepath (str): toml config file path.
    Returns:
        (str, int): host, port.
    """
    with open(filepath, "rb") as f:
        config = tomllib.load(f)

        host = config["server"]["host"]
        port = config["server"]["port"]
        return host, port
