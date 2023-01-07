import os
import pickle
import atexit
import aiofiles
from typing import Optional
from storages.async_storages.base_nosql_storage import BaseNoSQLStorage


def create_dir(file_path):
    dirs, filename = os.path.split(file_path)
    os.makedirs(dirs, exist_ok=True)
    if not os.path.isfile(file_path):
        with open(file_path, 'wb') as file:
            pickle.dump({}, file, protocol=pickle.HIGHEST_PROTOCOL)


class PickleStorage(BaseNoSQLStorage):
    def __init__(self, file_path: Optional[str]):
        super().__init__()
        self.file_path = file_path if file_path is not None else "./.storages/data.pkl"
        create_dir(self.file_path)

        atexit.register(self.dump)

    @classmethod
    async def create(cls, file_path: Optional[str]):
        obj = cls(file_path)
        await obj.load()
        return obj

    async def load(self):
        async with aiofiles.open(self.file_path, 'rb') as file:
            pickle_data = await file.read()
        self._data = pickle.loads(pickle_data)

    async def dump(self):
        async with aiofiles.open(self.file_path, 'wb') as file:
            pickle_data = pickle.dumps(self._data, protocol=pickle.HIGHEST_PROTOCOL)
            await file.write(pickle_data)
