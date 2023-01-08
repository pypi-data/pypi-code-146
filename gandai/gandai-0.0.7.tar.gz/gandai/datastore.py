import datetime
import json
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List

from google.cloud import storage


class Cloudstore:
    def __init__(self):
        self.bucket_name = os.getenv("BUCKET_NAME", "ph-gandai-dev")
        self.client = storage.Client(project=os.getenv("PROJECT_NAME", "gandai-dev"))
        self.bucket = self.client.get_bucket(self.bucket_name)

    def keys(self, prefix="") -> List[str]:
        keys = [
            blob.name
            for blob in self.client.list_blobs(self.bucket_name, prefix=prefix)
        ]
        return keys

    def __getitem__(self, key: str) -> json:
        blob = self.bucket.blob(key)
        return json.loads(blob.download_as_string())

    async def get(self, key: str) -> json:
        return self.__getitem__(key)

    def __setitem__(self, key: str, data) -> None:
        blob = self.bucket.blob(key)
        blob.upload_from_string(json.dumps(data))

    def load_async(self, keys):
        with ThreadPoolExecutor(max_workers=20) as exec:
            futures = exec.map(self.__getitem__, keys)
        return list(futures)

    def get_signed_url(self, key: str, hours_valid=72) -> str:
        blob = self.bucket.blob(key)
        expiration = datetime.timedelta(hours=hours_valid)
        url = blob.generate_signed_url(
            version="v4", expiration=expiration, method="GET"
        )
        return url
