"""S3 destination module for syncing files to S3"""
import io
import re
import threading

import boto3
import boto3.s3.transfer
import botocore.config
import botocore.exceptions

CHUNKSIZE = 8 << 20  # 8 MB
BOTO_CONFIG = botocore.config.Config(
    signature_version="s3v4", retries={"max_attempts": 3}
)
S3_TRANSFER_CONFIG = boto3.s3.transfer.TransferConfig(io_chunksize=CHUNKSIZE)
THREAD_LOCAL = threading.local()


class S3Destination:
    """S3 bucket/prefix sync destination"""

    def __init__(self, bucket, prefix=""):
        self.bucket = bucket
        # NOTE making sure prefix doesn't start but ends with slash for dir-like listing on s3
        self.prefix = (prefix.strip("/") + "/").lstrip("/")
        self.delete_lock = threading.Lock()
        self.delete_keys = []

    def __iter__(self):
        """Yield `S3File`s for objects found listing the destination bucket/prefix"""
        s3 = create_s3_client()
        paginator = s3.get_paginator("list_objects")
        for page in paginator.paginate(Bucket=self.bucket, Prefix=self.prefix):
            for content in page.get("Contents", []):
                yield self.file(
                    re.sub(rf"^{self.prefix}", "", content["Key"]).lstrip("/")
                )

    def check_perms(self):
        """Create/stat/delete a permcheck file - raise `PermissionError` on error"""
        try:
            s3 = create_s3_client()
            s3.head_bucket(Bucket=self.bucket)  # s3:HeadBucket (~ListBucket)
            file = self.file("permcheck")
            file.stat()  # s3:HeadObject
            file.store(io.BytesIO(b"permcheck"))  # s3:PutObject
            file.delete()
            self.cleanup()  # s3:DeleteObjects
        except botocore.exceptions.BotoCoreError as exc:
            raise PermissionError(f"Destination perm-check failed ({exc})") from exc

    def file(self, relpath):
        """Return an `S3File` for a given path relative to the destination bucket/prefix"""
        return S3File(self, relpath)

    def add_delete_key(self, key):
        """Add an S3 key  to `self.delete_keys` and call `cleanup()` at bulksize"""
        with self.delete_lock:
            self.delete_keys.append(key)
            if len(self.delete_keys) == 1000:
                self.cleanup()

    def cleanup(self):
        """Delete all S3 objects in `self.delete_keys` with a bulk delete request"""
        if self.delete_keys:
            s3 = create_s3_client()
            delete = {"Objects": [{"Key": key} for key in self.delete_keys]}
            s3.delete_objects(Bucket=self.bucket, Delete=delete)
            self.delete_keys = []


class S3File:
    """S3 file sync target"""

    __slots__ = ("name", "size", "modified", "s3dst", "key")

    def __init__(self, s3dst, relpath):
        self.name = relpath
        self.size = None
        self.modified = None
        self.s3dst = s3dst
        self.key = f"{s3dst.prefix}{relpath}"

    def stat(self):
        """Set self.size and modified via s3.head_object - return bool(file exists)"""
        s3 = create_s3_client()
        try:
            stat = s3.head_object(Bucket=self.s3dst.bucket, Key=self.key)
        except botocore.exceptions.ClientError:
            return False
        self.size, self.modified = (
            stat["ContentLength"],
            stat["LastModified"].timestamp(),
        )
        return True

    def store(self, src_file):
        """Upload S3 object with content from `src_file`"""
        s3 = create_s3_client()
        s3.upload_fileobj(
            src_file, self.s3dst.bucket, self.key, Config=S3_TRANSFER_CONFIG
        )

    def delete(self):
        """Add S3 object key to a list for later bulk deletion"""
        self.s3dst.add_delete_key(self.key)


def create_s3_client():
    """Create S3 client using default credentials (per thread)"""
    if not hasattr(THREAD_LOCAL, "s3"):
        THREAD_LOCAL.s3 = boto3.client("s3", config=BOTO_CONFIG)
    return THREAD_LOCAL.s3
