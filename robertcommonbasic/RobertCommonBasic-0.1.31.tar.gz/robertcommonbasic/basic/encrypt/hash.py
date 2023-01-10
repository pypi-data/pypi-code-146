import json
from hashlib import sha1
from typing import Union
from ..os.file import check_is_file


def file_hash(file_path: str):
    if check_is_file(file_path) is True:
        hash_sha1 = sha1()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha1.update(chunk)
        return hash_sha1.hexdigest()


def value_hash(content: Union[str, bytes, dict]):
    hash_sha1 = sha1()
    if isinstance(content, dict):
        content = json.dumps(content, ensure_ascii=False)

    if isinstance(content, str):
        content = content.encode()

    hash_sha1.update(content)
    return hash_sha1.hexdigest()
