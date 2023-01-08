"""Huawei obs function."""
import tomllib


def read_config(filepath, kind='obs'):
    """Read obs config from toml file.

    Args:
        filepath (str): toml config file path.
        kind (str): config kind, only obs now.
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
