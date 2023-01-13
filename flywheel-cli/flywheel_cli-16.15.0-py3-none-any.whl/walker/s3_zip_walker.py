"""S3 Zip Walker Module"""
import fs

from .s3_walker import S3Walker
from .zip_walker_mixin import ZipWalkerMixin


class S3ZipWalker(ZipWalkerMixin, S3Walker):
    """Walker that is implemented in terms of S3 and can extract files from zips"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._zip_meta = {}

    def _read_chunk(self, path, offset, size=None):
        """read chunk"""
        key = path
        if not key in self._zip_meta:
            key = fs.path.basename(path)
            if not key in self._zip_meta:
                raise ValueError(f"{path} not found in zip meta")

        if size:
            range_str = f"bytes={offset}-{offset+size}"
        else:
            range_str = f"bytes={offset}-"

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object
        response = self.client.get_object(Bucket=self.bucket, Key=key, Range=range_str)
        # https://botocore.amazonaws.com/v1/documentation/api/latest/reference/response.html#botocore.response.StreamingBody
        return response["Body"].read()
