from __future__ import annotations

from typing import TYPE_CHECKING

from vectice.models.datasource.datawrapper.data_wrapper import DataWrapper
from vectice.models.datasource.datawrapper.metadata.files_metadata import DatasetSourceUsage, File, FilesMetadata
from vectice.models.datasource.datawrapper.metadata.metadata import SourceOrigin

if TYPE_CHECKING:
    from mypy_boto3_s3 import Client
    from mypy_boto3_s3.type_defs import ListObjectsV2OutputTypeDef, ObjectTypeDef


class S3DataWrapper(DataWrapper):
    """Wrap columnar data and its metadata in AWS S3.

    Implements :py:class:`DataWrapper`.

    """

    def __init__(
        self,
        s3_client: Client,
        bucket_name: str,
        resource_path: str,
        name: str,
        usage: DatasetSourceUsage | None = None,
        inputs: list[int] | None = None,
        capture_code: bool = True,
    ):
        """
        :param s3_client: the client used to interact with Amazon s3
        :param bucket_name: the name of the bucket to get data from
        :param resource_path: the paths of the resources to get
        :param usage: The usage of the dataset
        :param name: The name of the :py:class:`DataWrapper`
        :param inputs: The list of dataset ids to create a new dataset from
        """
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.resource_path = resource_path
        super(S3DataWrapper, self).__init__(name, usage, inputs, capture_code)

    def _fetch_data(self) -> dict[str, bytes]:
        s3_objects_list = self._get_s3_objects_list()
        datas = {}
        for s3_object in s3_objects_list["Contents"]:
            object_path = s3_object["Key"]
            data = self._get_aws_data(object_path)
            datas[f"{self.bucket_name}/{object_path}"] = data
        return datas

    def _get_aws_data(self, object_path: str):
        data_response = self.s3_client.get_object(Bucket=self.bucket_name, Key=object_path)
        return data_response["Body"].read()

    def _build_metadata(self) -> FilesMetadata:
        s3_objects_list = self._get_s3_objects_list()
        metadata = self._build_metadata_from_objects(s3_objects_list)
        return metadata

    def _get_s3_objects_list(self) -> ListObjectsV2OutputTypeDef:
        return self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=self.resource_path)

    def _build_metadata_from_objects(self, s3_objects_list: ListObjectsV2OutputTypeDef) -> FilesMetadata:
        if s3_objects_list["KeyCount"] == 0:
            raise NoSuchS3ResourceError(self.bucket_name, self.resource_path)
        s3_objects = s3_objects_list["Contents"]
        files, total_size = self._build_files_list_with_size(s3_objects)
        metadata = FilesMetadata(
            files=files, origin=SourceOrigin.S3, files_count=len(files), size=total_size, usage=self.usage
        )
        return metadata

    def _build_files_list_with_size(self, s3_objects: list[ObjectTypeDef]) -> tuple[list[File], int]:
        files: list[File] = []
        total_size = 0
        for object in s3_objects:
            if not self._is_s3_object_a_folder(object):
                name = object["Key"]
                size = object["Size"]
                file = File(
                    name=name,
                    size=size,
                    fingerprint=self._get_formatted_etag_from_object(object),
                    updated_date=object["LastModified"].isoformat(),
                    created_date=None,
                    uri=f"s3://{self.bucket_name}/{name}",
                )
                total_size += size
                files.append(file)
        return files, total_size

    @staticmethod
    def _get_formatted_etag_from_object(object: ObjectTypeDef) -> str:
        return str(object["ETag"].replace("'", "").replace('"', ""))

    @staticmethod
    def _is_s3_object_a_folder(object: ObjectTypeDef) -> bool:
        return bool(object["Key"].endswith("/"))


class NoSuchS3ResourceError(Exception):
    def __init__(self, bucket: str, resource: str):
        self.message = f"{resource} does not exist in the AWS s3 bucket {bucket}."
        super().__init__(self.message)

    def __str__(self):
        return self.message
