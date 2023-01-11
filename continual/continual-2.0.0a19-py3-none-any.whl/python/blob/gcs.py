import os
import logging
import urllib.parse
from urllib.parse import urlparse
from urllib3.exceptions import ProtocolError
from requests.exceptions import ChunkedEncodingError
from google.cloud import storage
from google.api_core import retry

logger = logging.getLogger(__name__)


class GoogleCloudStorage(object):
    def __init__(self, resource_url, **kwargs):
        self.resource_url = resource_url
        self._register_gcs_scheme()

        # GCS has a download timeout of 60s. There doesn't seem to be a
        # way to alter it but we can download in chunks.
        storage.blob._DEFAULT_CHUNKSIZE = 100 * 1024 * 1024  # 100M
        storage.blob._MAX_MULTIPART_SIZE = 100 * 1024 * 1024  # 100M

        self.bucket_name = kwargs.get("bucket_name", self._parse_bucket_name())

        if "project" in kwargs or "credentials" in kwargs:
            self.client = storage.Client(
                project=kwargs.get("project"), credentials=kwargs.get("credentials")
            )
        else:
            self.client = storage.Client()

    @staticmethod
    def is_valid_url(resource_url):
        if not resource_url.startswith("gs://"):
            logger.warning("resource URL does not start with gs://")
            return False
        elif not resource_url[len("gs://") :]:
            logger.warning("resource URL does not contain bucket name after gs://")
            return False

        return True

    def list_objects(self):
        blobs = self.client.list_blobs(
            self.bucket_name, prefix=self._get_path_from_url(self.resource_url)
        )
        objs = []
        for b in blobs:
            if b.name.endswith("/"):
                continue
            objs.append(b.name)
        return objs

    def _register_gcs_scheme(self):
        def register_scheme(scheme):
            for method in filter(lambda s: s.startswith("uses_"), dir(urllib.parse)):
                getattr(urllib.parse, method).append(scheme)

        register_scheme("gs")

    def _parse_bucket_name(self):
        parts = urlparse(self.resource_url)._asdict()
        bucket = parts.get("netloc")  # gs://bucket => bucket
        if not bucket:
            raise ValueError(
                "cannot extract bucket name from resource URL, found {}".format(bucket)
            )
        return bucket

    def _get_or_create_bucket(self, bucket_name=""):
        bucket_name = bucket_name or self.bucket_name
        try:
            bucket = self.client.get_bucket(bucket_name)
            logger.info("bucket already exists with name {}...".format(bucket_name))
            return bucket
        except Exception as e:
            logger.info(
                f"Encountered exception [{e}] for bucket [{bucket_name}], will try to create it"
            )
            bucket = self.client.create_bucket(bucket_name)
            return bucket

    def _get_path_from_url(self, url: str) -> str:
        parts = urlparse(url)._asdict()
        path = str(parts.get("path"))
        if path and path[0] == "/":
            path = path[1:]

        return path

    def upload_file(self, filepath, prefix="", bucket_name="", bucket=None):
        bucket_name = bucket_name or self.bucket_name
        if not bucket:
            bucket = self._get_or_create_bucket(bucket_name)

        filename = os.path.split(filepath)[-1]
        blob_name = os.path.join(prefix, filename)
        blob = bucket.blob(blob_name)

        logger.info("Uploading ({}) to ({})".format(filepath, blob_name))
        blob.upload_from_filename(filepath)
        logger.info("Uploaded ({}) to ({})".format(filepath, blob_name))

    def upload_dir(self, dirpath: str, prefix: str = "", bucket_name: str = "") -> None:
        logger.info("Uploading files recursively from directory: ({})".format(dirpath))
        bucket_name = bucket_name or self.bucket_name
        bucket = self._get_or_create_bucket(bucket_name)

        for root, _dirs, files in os.walk(dirpath):
            for file in files:
                nested_prefix = os.path.relpath(root, dirpath)
                if nested_prefix == ".":
                    nested_prefix = ""

                nested_prefix = os.path.join(prefix, nested_prefix)

                self.upload_file(
                    os.path.join(root, file),
                    prefix=nested_prefix,
                    bucket_name=bucket_name,
                    bucket=bucket,
                )
        return

    def download_file(
        self, blobpath, outpath="", bucket_name="", bucket=None, base_name=""
    ):
        bucket_name = bucket_name or self.bucket_name
        if not bucket:
            bucket = self._get_or_create_bucket(bucket_name)

        if self.is_valid_url(blobpath):
            blobpath = self._get_path_from_url(blobpath)

        blob = bucket.get_blob(blobpath)
        if not blob:
            raise Exception("could not find blob to download: {}".format(blobpath))

        blobname = blob.name[len(base_name) + 1 :]
        if base_name == "":
            blobname = blob.name.split("/")[-1]
        dl_path = os.path.join(outpath, blobname)
        path = "/"
        path = path.join(dl_path.split("/")[:-1])
        if not os.path.isdir(path):
            print("making path: " + path)
            os.makedirs(path)

        retrier = retry.Retry(
            predicate=retry.if_exception_type(
                ConnectionResetError,
                ProtocolError,
                ChunkedEncodingError,
            ),
        )
        retrier(blob.download_to_filename)(dl_path)

        return dl_path

    def download_as_string(self, blobpath=None):
        bucket = self._get_or_create_bucket(None)
        if blobpath is not None and self.is_valid_url(blobpath):
            blobpath = self._get_path_from_url(blobpath)
        else:
            blobpath = self._get_path_from_url(self.resource_url)

        if blobpath is None:
            raise ValueError(f"No blob name in path [{blobpath}]")

        blob = bucket.get_blob(blobpath)
        if not blob:
            raise ValueError("could not find blob to download: [{}]".format(blobpath))

        ret_str = blob.download_as_string()
        return ret_str

    def download_dir(
        self, dirpath: str, outpath: str = "", bucket_name: str = ""
    ) -> str:
        bucket_name = bucket_name or self.bucket_name
        bucket = self._get_or_create_bucket(bucket_name)

        if self.is_valid_url(dirpath):
            dirpath = self._get_path_from_url(dirpath)

        blobs = bucket.list_blobs(prefix=dirpath)

        for blob in blobs:

            blobname = blob.name
            self.download_file(
                blobname,
                outpath=outpath,
                bucket_name=bucket_name,
                bucket=bucket,
                base_name=dirpath,
            )

        return os.path.join(outpath, dirpath)
