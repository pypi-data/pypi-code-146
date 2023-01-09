import hashlib
import json
import os
import warnings
from pathlib import Path
from typing import Union

from pymbse.query.config.numpy_encoder import NumpyEncoder  # type: ignore


def hash_dict(dict_to_hash: dict) -> str:
    """Function hashing a dictionary with md5 algorithm

    :param dict_to_hash: a dictionary with content to be hashed
    :return: an md5 hash of a dictionary
    """
    return hashlib.md5(
        json.dumps(dict_to_hash, sort_keys=True, cls=NumpyEncoder).encode("utf-8")
    ).hexdigest()


def hash_file(abs_path: Union[Path, str]) -> str:
    """Function hashing a file based on its content with md5 hash algorithm
    :param abs_path: an absolute path to a file
    :return: a string with md5 hash
    """
    if not os.path.isfile(abs_path):
        warnings.warn(
            f"Can't hash an input file {abs_path} as it does not exist. "
            f"Either create the file or change model_configuration.yml definition."
        )
        return hashlib.md5("".encode("utf-8")).hexdigest()

    with open(abs_path, "rb") as file:
        return hashlib.md5(file.read()).hexdigest()
