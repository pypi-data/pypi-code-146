import os
import json
import atexit
from typing import Optional
from storages.sync_storages.base_nosql_storage import BaseNoSQLStorage


def create_dir(file_path):
    dirs, filename = os.path.split(file_path)
    os.makedirs(dirs, exist_ok=True)
    if not os.path.isfile(file_path):
        with open(file_path, 'w') as file:
            json.dump({}, file)


class JSONStorage(BaseNoSQLStorage):
    def __init__(self, file_path: Optional[str]):
        super().__init__()
        self.file_path = file_path if file_path is not None else "./.storages/data.json"
        create_dir(self.file_path)
        self.load()

        atexit.register(self.dump)

    def load(self):
        with open(self.file_path, 'r') as file:
            self._data = json.load(file)

    def dump(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file)
