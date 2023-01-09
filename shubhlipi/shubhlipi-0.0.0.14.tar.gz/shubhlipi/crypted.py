import base64
import hashlib
import uuid
from .kry import get_type, from_base64, to_base64
try:
    from cryptography.fernet import Fernet
except:
    pass


def bin_str(val) -> str:
    if get_type(val) == "bytes":
        return val
    else:
        return bytes(val, "utf-8")


def salt() -> str:
    return uuid.uuid4().hex


def hash_256(val) -> str:
    return hashlib.sha3_256(bin_str(val)).hexdigest()


def hash_512(val) -> str:
    return hashlib.sha3_512(bin_str(val)).hexdigest()


def hash_md5(val) -> str:
    return hashlib.md5(bin_str(val)).hexdigest()


def encrypt(val, key: str) -> bytes:
    """Used to encrypt `bytes` or `str`"""
    f = Fernet(to_base64(hash_md5(key)))
    return f.encrypt(bin_str(val))


def decrypt(val, key: str) -> bytes:
    f = Fernet(to_base64(hash_md5(key)))
    return f.decrypt(bin_str(val))


def decrypt_text(val, key: str):
    return decrypt(val, key).decode("utf-8")
