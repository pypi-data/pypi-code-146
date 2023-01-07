"""Huawei Object Based Storage (OBS) backend."""
from obs import ObsClient, PutObjectHeader


class Client:
    """Huawei Object Based Storage (OBS) backend."""

    def __init__(self, access_key, secret_key, endpoint):
        """Initialize the OBS backend.

        Args:
            access_key(str): OBS access key.
            secret_key (str): OBS secret access key.
            endpoint (str): OBS server address. e.g. https://obs.cn-north-1.myhwclouds.com
        """

        self.obs = ObsClient(access_key, secret_key, server=endpoint)

    def add(self, bucket, filename, content_type, file):
        """Add file to OBS.

        Args:
            bucket (str): OBS bucket name.
            filename (str): filename.
            content_type (str): image MIME type / media type e.g. image/png or text/markdown.
            file (File) :  A SpooledTemporaryFile (a file-like object).
            This is the actual Python file that you can pass directly to other functions
            or libraries that expect a "file-like" object.
        """
        # check is has same file
        result = self.obs.getObjectMetadata(bucket, filename)
        if result.status < 300:
            # has same file
            return False

        # upload file to obs
        headers = PutObjectHeader(contentType=content_type)
        result = self.obs.putContent(bucket, filename, file, headers)

        # upload success
        if result.status < 300:
            # return true and file url
            return True, result.body.objectUrl

        # upload failed, return false and error message
        return False, result.reason

    def delete(self, bucket, filename):
        """Delete file from OBS.

        Args:
            bucket (str): OBS bucket name.
            filename (str): filename
        """
        result = self.obs.deleteObject(bucket, filename)

        # delete success
        if result.status < 300:
            return True

        # delete failed
        return False

    def get_object(self, bucket, filename):
        """Get file from OBS.

        Args:
            bucket (str): OBS bucket name.
            filename (str): filename
        """
        return self.obs.getObject(bucket, filename, loadStreamInMemory=True)
