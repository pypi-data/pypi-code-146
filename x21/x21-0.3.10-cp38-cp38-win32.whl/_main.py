from __future__ import annotations

import base64
import random
import secrets
import string
import sys

import _x21


def encrypt_source(source: str) -> str:
    # if path.suffix != ".py":
    #     raise ValueError("Must be .py file")
    #
    # with open(path) as f:
    #     content = f.read()

    iv = _get_random_string(16)
    scode = _encrypt("22b", source, iv)
    return f"""from x21 import __dex_22b__

__dex_22b__(
    globals(),
    "{iv}",
    {scode}
)"""

    # with open(path, "w") as f:
    #     f.write(content)


def _get_random_string(length: int, seed: int | None = None) -> str:
    """
    Returns random alphanumeric string.
    """
    if seed is not None:
        random.seed(seed)
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def _get_random_bytes(nbytes: int, seed: int | None = None) -> bytes:
    if seed is not None:
        random.seed(seed)
        try:
            # Python 3.9+
            return random.randbytes(nbytes)
        except AttributeError:
            return random.getrandbits(nbytes * 8).to_bytes(nbytes, sys.byteorder)

    return secrets.token_bytes(nbytes)


def _encrypt(key_tag: str, message: str, iv: str | bytes) -> bytes | str:
    if key_tag == "23a":
        assert isinstance(iv, bytes)
        assert len(iv) == 12
        iv_smessage_tag = _x21.encrypt_23a(message, iv)
        return base64.a85encode(iv_smessage_tag)

    elif key_tag == "22b":
        assert len(iv) == 16
        return _x21.encrypt_22b(message, iv)

    elif key_tag == "22a":
        raise ValueError("Need x21 < 0.3")

    else:
        raise ValueError(f"Unknown key {key_tag}")


def __dex__(glob: dict, key_tag: str, smessage: bytes) -> None:
    assert key_tag == "22a"
    raise ValueError("Need x21 < 0.3")


def __dex_22b__(glob: dict, iv: bytes, smessage: bytes) -> None:
    _x21.decrypt_and_exec_22b(smessage, iv, glob)


def __dex_23a__(glob: dict, iv_smessage_tag: str) -> None:
    data = base64.a85decode(iv_smessage_tag)
    _x21.decrypt_and_exec_23a(data, glob)
