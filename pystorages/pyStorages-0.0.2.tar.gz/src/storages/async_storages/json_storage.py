import os
import json
import atexit
import aiofiles
from typing import Optional
from storages.async_storages.base_nosql_storage import BaseNoSQLStorage


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

        atexit.register(self.dump)

    @classmethod
    async def create(cls, file_path: Optional[str]):
        obj = cls(file_path)
        await obj.load()
        return obj

    async def load(self):
        async with aiofiles.open(self.file_path, 'r') as file:
            json_data = await file.read()
        self._data = json.loads(json_data)

    async def dump(self):
        async with open(self.file_path, 'w') as file:
            json_data = json.dumps(self._data)
            await file.write(json_data)
