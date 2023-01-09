from datetime import datetime
from pathlib import Path
import os


def add_years(start_date, years):
    try:
        return start_date.replace(year=start_date.year + years)
    except ValueError:
        # preserve calendar day (If Feb 29th doesn't exist, set to Feb 28th)
        return start_date.replace(year=start_date.year + years, day=28)


def read_rsa_key(key_file: str, fmt: str = "pem") -> bytes:
    """read in private rsa key file for signing roa requests

    Parameters:
        key_file: str - path to file that holds the key
        fmt: str - format of the key, default = pem
    """
    key_file_path = Path(key_file)

    if not key_file_path.exists():
        raise FileNotFoundError(key_file)

    header_trailer = [
        "-----BEGIN RSA PRIVATE KEY-----",
        "-----END RSA PRIVATE KEY-----",
    ]
    contents = key_file_path.read_text()
    # remove the start and end markers, make all one line
    contents = contents.replace(os.linesep, "")
    contents = contents.replace("\n", "")
    contents = contents.strip()
    contents = contents.replace("-----BEGIN RSA PRIVATE KEY-----", "")
    contents = contents.replace("-----END RSA PRIVATE KEY-----", "")

    return contents


def gen_signature(private_key: str, message: str):
    """Generate a base64 serialized signature for a str"""
    signing_key = SigningKey(private_key, encoder=Base64Encoder)
    return signing_key.sign(message)
