from continual.python.blob.gcs import GoogleCloudStorage


class BlobStore(object):

    SUPPORTED_STORES = [GoogleCloudStorage]

    def __init__(self, resource_url, **kwargs):
        self.resource_url = resource_url
        self._kwargs = kwargs
        self.store = self._validate_url(resource_url)

    def _validate_url(self, resource_url):
        ValidStore = None
        for s in self.SUPPORTED_STORES:
            if s.is_valid_url(resource_url):
                ValidStore = s
                break

        if not ValidStore:
            raise ValueError(
                "Invalid URL. No supported blob stores support this resource URL."
            )

        return ValidStore(resource_url, **self._kwargs)

    def list_objects(self):
        if not self.store:
            raise ValueError(
                "Cannot list objects - blob store has not been initialized."
            )

        return self.store.list_objects()

    def upload_file(self, filepath, **kwargs):
        if not self.store:
            raise ValueError("Cannot upload - blob store has not been initialized.")

        return self.store.upload_file(filepath, **kwargs)

    def upload_dir(self, dirpath, **kwargs):
        if not self.store:
            raise ValueError("Cannot upload - blob store has not been initialized.")

        return self.store.upload_dir(dirpath, **kwargs)

    def download_file(self, filepath=None, **kwargs):
        if not self.store:
            raise ValueError("Cannot download — blob store has not been initialized.")

        return self.store.download_file(filepath, **kwargs)

    def download_as_string(self, filepath=None, **kwargs):
        if not self.store:
            raise ValueError("Cannot download — blob store has not been initialized.")

        return self.store.download_as_string(filepath, **kwargs)

    def download_dir(self, dirpath, **kwargs):
        if not self.store:
            raise ValueError("Cannot download — blob store has not been initialized.")

        return self.store.download_dir(dirpath, **kwargs)
