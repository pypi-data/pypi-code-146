import shutil
from functools import lru_cache
from pathlib import Path

from minio import Minio
from minio.error import S3Error

from blx.cache import cache
from blx.cid import CID
from blx.env import env
from blx.progress import Progress

__all__ = ["Client", "get_client"]


class Client:
    def __init__(self):
        self._minio = get_minio()

    def has(self, cid: CID):
        try:
            self._minio.stat_object(env.BLX_BUCKET, cid.hex())
        except S3Error as err:
            if err.code == "NoSuchKey":
                return False
            else:
                raise err
        return True

    def put(self, cid: CID, input: Path, progress: Progress):
        file = str(input.resolve())
        self._minio.fput_object(env.BLX_BUCKET, cid.hex(), file, progress=progress)

    def get(self, cid: CID, output: Path, progress: Progress):
        if cache.has(cid):
            shutil.copyfile(cache.get(cid), output)
            progress.set_completed()
            return
        file = str(output.resolve())
        self._minio.fget_object(env.BLX_BUCKET, cid.hex(), file, progress=progress)
        cache.put(cid, output)


@lru_cache
def get_client():
    return Client()


@lru_cache
def get_minio():
    return Minio(
        env.BLX_HOST, access_key=env.BLX_ACCESS_KEY, secret_key=env.BLX_SECRET_KEY
    )
