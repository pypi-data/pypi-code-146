import pathlib
from base64 import b64encode


def read_file_to_b64(path: str):
    """Read a string in base64-encoded format

    This helper method is used in the SDK when a provided input needs to be base64 encoded (for example, when providing the certificate and private key to create a fiscal link).

    Args:
        path (str): The string to read and convert.

    Raises:
        ValueError: If the provided file is not a string, raises a ValueError.

    Returns:
        The string in base64-encoded format.
    """
    file = pathlib.Path(path)
    if file.exists() and file.is_file():
        with open(path, "rb") as fr:
            return b64encode(fr.read())
    else:
        raise ValueError("Invalid file path")
