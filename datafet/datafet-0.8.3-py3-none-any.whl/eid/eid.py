import base64
import random
import re

import spookyhash
from blake3 import blake3


def get_external_id_bytes(b: bytes, prefix: str) -> str:
    h64 = spookyhash.hash64(b, seed=1337).to_bytes(8, byteorder="little").hex()
    b32 = base64.b32encode(h64.encode("utf-8")).decode("utf-8")
    result = re.sub("=", "", b32.lower())
    return f"{prefix}-{result}"


def get_external_id_str(name: str, prefix: str) -> str:
    byt = str.encode(name)
    return get_external_id_bytes(byt, prefix)


def get_db_eid(database_name: str) -> str:
    return get_external_id_str(database_name, "db")


def get_table_eid(table_name: str) -> str:
    return get_external_id_str(table_name, "table")


def get_job_eid(job_name: str) -> str:
    return get_external_id_str(job_name, "job")


def get_req_eid() -> str:
    byt = random.randbytes(16)
    return get_external_id_bytes(byt, "req")


def get_external_id_bytes_blake3(b: bytes, prefix: str) -> str:
    hash = blake3(b).digest(length=16)
    b32 = base64.b32encode(hash).decode("utf-8")
    result = re.sub("=", "", b32.lower())
    return f"{prefix}-{result}"


def get_external_id_str_blake3(name: str, prefix: str) -> str:
    byt = str.encode(name)
    return get_external_id_bytes_blake3(byt, prefix)


def get_org_eid(email_domian: str) -> str:
    return get_external_id_str_blake3(email_domian, "org")


def get_user_eid(email_address: str) -> str:
    return get_external_id_str_blake3(email_address, "user")


def get_eval_eid() -> str:
    byt = random.randbytes(16)
    return get_external_id_bytes_blake3(byt, "eva")


def get_mat_eid() -> str:
    byt = random.randbytes(16)
    return get_external_id_bytes_blake3(byt, "mat")
