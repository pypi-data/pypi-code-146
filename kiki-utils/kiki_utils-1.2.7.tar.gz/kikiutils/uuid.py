from uuid import uuid1

from .file import read_file, save_file


# UUID

def get_uuid(save_path: str = './uuid.uuid'):
    if now_uuid := read_file(save_path):
        return now_uuid.decode()

    now_uuid = str(uuid1())
    save_file(save_path, now_uuid)
    return now_uuid
