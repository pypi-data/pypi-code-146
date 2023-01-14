import base64
import hashlib

Base64str = str


def base64encode(to_encode: str) -> Base64str:
    return base64.b64encode(to_encode.encode("UTF-8")).decode("UTF-8")


def sha1(to_sha: str) -> str:
    sha1_algo = hashlib.sha1()
    sha1_algo.update(to_sha.encode("UTF-8"))
    return sha1_algo.hexdigest()
