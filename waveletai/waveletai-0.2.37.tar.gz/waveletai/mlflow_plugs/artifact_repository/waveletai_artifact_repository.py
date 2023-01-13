# @Time    : 2021/6/23 17:47
# @Author  : Boyang
# @Site    : 
# @File    : waveletai_artifact_repository.py
# @Software: PyCharm
import os
import posixpath
from mimetypes import guess_type

from six.moves import urllib

from mlflow.store.artifact.artifact_repo import ArtifactRepository

import waveletai


class WaveletAIArtifactRepository(ArtifactRepository):
    def __init__(self, artifact_uri):
        super(WaveletAIArtifactRepository, self).__init__(artifact_uri)

    @staticmethod
    def parse_uri(uri):
        """Parse an S3 URI, returning (bucket, path)"""
        parsed = urllib.parse.urlparse(uri)
        if parsed.scheme != "waveletai-artifact-repository":
            raise Exception("Not an waveletai-artifact-repository URI: %s" % uri)
        path = parsed.path
        if path.startswith("/"):
            path = path[1:]
        return parsed.netloc, path

    def _upload_file(self, local_file, artifact_path):
        extra_args = dict()
        guessed_type, guessed_encoding = guess_type(local_file)
        if guessed_type is not None:
            extra_args["ContentType"] = guessed_type
        if guessed_encoding is not None:
            extra_args["ContentEncoding"] = guessed_encoding

        waveletai.upload_artifact(local_file=local_file, artifact_path=artifact_path, run_id=self._get_run_id())

    def _get_run_id(self):
        (bucket, dest_path) = self.parse_uri(self.artifact_uri)
        return dest_path.split('/')[-2]

    def log_artifact(self, local_file, artifact_path=None):
        if posixpath.isfile(local_file) and artifact_path:
            artifact_path = posixpath.join(artifact_path, os.path.basename(local_file))
        self._upload_file(local_file=local_file, artifact_path=artifact_path)

    def log_artifacts(self, local_dir, artifact_path=None):
        self._upload_file(local_file=local_dir, artifact_path=artifact_path)

    def list_artifacts(self, path):
        pass

    def _download_file(self, remote_file_path, local_path):
        pass
