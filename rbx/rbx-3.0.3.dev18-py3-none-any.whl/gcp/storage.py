import logging

from google.cloud.storage import Client

logger = logging.getLogger(__name__)


class Storage:
    """Provides functionality to upload/download content to/from GCS."""

    def __init__(self, project_id, bucket=None):
        self.client = Client()
        self.bucket = self.client.get_bucket(bucket or f"{project_id}.appspot.com")

    def download(self, location):
        blob = self.bucket.blob(location)
        if blob.exists():
            logger.debug(f'Downloading from storage: "{blob.name}"')
            content = blob.download_as_string()
            return content.decode("utf-8")

    def list_objects(self, prefix=None):
        """Return an iterator of all objects in the bucket matching the prefix.

        The objects are returned as bytes.
        """
        for blob in self.bucket.list_blobs(prefix=prefix.lstrip("/")):
            yield blob.download_as_string()

    def upload(self, content, location, content_type="text/plain"):
        blob = self.bucket.blob(location.lstrip("/"))
        logger.debug(f'Uploading to storage: "{blob.name}"')
        blob.upload_from_string(content.encode("utf-8"), content_type=content_type)
