import base64
import os
import secrets


def get_config_value(config, key1, key2, default=None):
    if not key1 in config:
        return default
    inner_config = config[key1]
    if not key2:
        return inner_config
    if not key2 in inner_config:
        return default
    return inner_config[key2]


def get_config_value_arbitrary_depth(config, keys, default):
    for key in keys:
        if not key in config:
            return default
        config = config[key]

    return config


def get_token_secret_and_algorithm(secret_file_path, *, logger=None):
    token_secret_file = os.path.expandvars(secret_file_path)

    jwt_encode_secret = None

    if os.path.isfile(token_secret_file):
        with open(token_secret_file, 'rb') as fp:
            jwt_encode_secret = base64.standard_b64decode(fp.read())
    else:
        msg = "Secret file does not exist, secret generated, but will not work upon restart."
        if logger:
            logger.warning(msg)
        else:
            print(msg)
        jwt_encode_secret = secrets.token_hex(512)
    jwt_token_algorithm = 'HS512'

    return jwt_encode_secret, jwt_token_algorithm
