import hashlib


def generate_uuid(string: str) -> str:
    h = hashlib.sha256()
    h.update(bytes(string, 'utf-8'))

    return str(h.hexdigest())
