"""Object Based Storage (OBS) backend."""
from obs import ObsClient, PutObjectHeader


class Client:
    """Object Based Storage (OBS) backend.



    """

    def __init__(self, credentials):
        """Initialize the OBS backend.

        :param access_key: OBS access key.
        :type access_key: str
        :param secret_key: OBS secret access key.
        :type secret_key: str
        :param endpoint: OBS server address. e.g. https://obs.cn-north-1.myhwclouds.com
        :type endpoint: str
        """

        # self.obs = ObsClient(access_key, secret_key, server=endpoint)

    def add(self, bucket, filename, content_type, file):
        """Add file to OBS.

        :param bucket: OBS bucket name.
        :type bucket: str
        :param filename: filename.
        :type filename: str
        :param content_type: image MIME type / media type e.g. image/png or text/markdown.
        :type content_type: str
        :param file: A SpooledTemporaryFile (a file-like object).
            This is the actual Python file that you can pass directly to other functions
            or libraries that expect a "file-like" object.
        :type file: File

        :return: if success return (True, url), else return (False, reason)
        :rtype: (bool, str)
        """
        # check is has same file
        result = self.obs.getObjectMetadata(bucket, filename)
        if result.status < 300:
            # has same file
            return False, "has same file"

        # upload file to storage
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

        :param bucket: OBS bucket name.
        :type bucket: str
        :param filename: filename
        :type filename: str

        :return: if success return (True, message), else return (False, reason)
        :rtype: (bool, str)
        """
        result = self.obs.deleteObject(bucket, filename)

        # delete success
        if result.status < 300:
            return True, "delete success"

        # delete failed
        return False, result.reason

    def get(self, bucket, filename):
        """Get file from OBS.

        :param bucket: OBS bucket name.
        :type bucket: str
        :param filename: filename
        :type filename: str

        :return: if success return (True, file), else return (False, reason)
        :rtype: (bool, str)
        """
        result = self.obs.getObject(bucket, filename, loadStreamInMemory=True)

        if result.status < 300:
            return True, result.body["contentType"],  result.body.buffer

        return False, result.reason, ""
