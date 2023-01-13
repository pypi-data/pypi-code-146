# -*- coding: utf-8 -*-
""" API for AWS Content Management """


from typing import List
from typing import Optional

from baseblock import EnvIO
from baseblock import BaseObject

from awsfile_helper.svc import ConnectToS3
from awsfile_helper.svc import ReadFromS3
from awsfile_helper.svc import FindLatestVersionNumber
from awsfile_helper.svc import DownloadFromS3
from awsfile_helper.svc import CreateBucketFolder
from awsfile_helper.svc import FindFileByVersion
from awsfile_helper.svc import UploadImageFiles


class AwsAPI(BaseObject):
    """ API for AWS Content Management """

    def __init__(self,
                 aws_access_key: Optional[str] = None,
                 aws_secret_key: Optional[str] = None):
        """ Change Log

        Created:
            22-Jul-2022
            craigtrim@gmail.com
            *   https://bast-ai.atlassian.net/browse/COR-8
        Updated:
            5-Aug-2022
            craigtrim@gmail.com
            *   adhere to latest standard on file version
                https://bast-ai.atlassian.net/browse/COR-59
        Updated:
            11-Nov-2022
            craigtrim@gmail.com
            *   pass keys as parameters
                https://github.com/craigtrim/awsfile-helper/issues/4
        Updated:
            17-Nov-2022
            craigtrim@gmail.com
            *   add additional logging statements

        Args:
            aws_access_key (str, Optional): Encrypted AWS Access Key
                if the key is not provided as a parameter,
                it must be encrypted within the environment as AWS_ACCESS_KEY
            aws_secret_key (str, Optional): Encrypted AWS Secret Key
                if the key is not provided as a parameter,
                it must be encrypted within the environment as AWS_SECRET_KEY
        """
        BaseObject.__init__(self, __name__)

        self._s3_resource = ConnectToS3(  # S3 Resource ...
            aws_access_key=aws_access_key,
            aws_secret_key=aws_secret_key).resource()

        self._s3_client = ConnectToS3(  # S3 Client ...
            aws_access_key=aws_access_key,
            aws_secret_key=aws_secret_key).client()

        self._read_files = ReadFromS3(self._s3_resource).process
        self._find_latest_version_number = FindLatestVersionNumber(
            self._read_files).process

        self._download_files = DownloadFromS3(self._s3_resource).process
        self._find_file_by_version = FindFileByVersion(
            self._download_files).process
        self._create_folder = CreateBucketFolder(self._s3_client).process
        self._upload_images = UploadImageFiles(self._s3_client).process

    def read_files(self,
                   bucket_name: str,
                   file_name: str,
                   load_files: bool = True) -> dict:
        """ Open and Read S3 Files

        Args:
            bucket_name (str): the name of the S3 bucket
            file_name (str): the file name (or prefix) to search for
            load_files (bool): load the contents of the input files
                if None, the keyed value will be None

        Returns:
            dict: a dictionary of file contents keyed by file name
        """
        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                'Reading Files',
                f'\tBucket Name: {bucket_name}',
                f'\tFile Name: {file_name}',
                f'\tLoad Files? {load_files}']))

        return self._read_files(
            file_name=file_name,
            bucket_name=bucket_name,
            load_files=load_files)

    def download_files(self,
                       bucket_name: str,
                       file_name: str) -> dict:
        """ Persist S3 Files to Local Directory

        Args:
            bucket_name (str): the name of the S3 bucket
            file_name (str): the file name (or prefix) to search for

        Returns:
            dict: a dictionary of file paths keyed by file name
        """
        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                'Downloading Files',
                f'\tBucket Name: {bucket_name}',
                f'\tFile Name: {file_name}']))

        return self._download_files(
            file_name=file_name,
            bucket_name=bucket_name)

    def latest_version_number(self,
                              bucket_name: str,
                              file_name: str) -> str or None:
        """ Get the Latest Version of a File

        Args:
            bucket_name (str): the name of the bucket
                e.g., name-of-bucket
            file_name (str): the qualified name of the file
                e.g., 'training/myeliza/doctor'

        Returns:
            str or None: the latest version
                e.g., '0.1.2'
        """
        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                'Finding Latest Version Number',
                f'\tBucket Name: {bucket_name}',
                f'\tFile Name: {file_name}']))

        return self._find_latest_version_number(
            bucket_name=bucket_name,
            file_name=file_name)

    def file_by_version(self,
                        bucket_name: str,
                        file_name: str,
                        file_ext: str,
                        version: str = None) -> str:
        """ Download a versioned Bast S3 file to a local directory

        Args:
            bucket_name (str): the name of the bucket
                e.g., name-of-bucket
            file_name (str): the qualified name of the file
                e.g., 'training/myeliza/doctor'
            file_ext (str): the file extension
                e.g., 'txt'
            version (str, optional): the version of the file to access
                e.g., '0.1.0'
                if the version is not provided as a parameter, the value will be retrieved from the environment
                    - the file_name will be used as the key
                if the version is not provided in the environment, the value will default to '*'
                    - the use of '*' signifies the service should retrieve the latest version

        Returns:
            str: the local path of the downloaded S3 file
        """

        if not version or not len(version):
            version = EnvIO.str_or_default(file_name, '*')

        if version == '*':
            version = self.latest_version_number(
                bucket_name=bucket_name,
                file_name=file_name)

        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                'Finding File By Version',
                f'\tBucket Name: {bucket_name}',
                f'\tFile Name: {file_name}',
                f'\tFile Ext: {file_ext}',
                f'\tVersion: {version}']))

        return self._find_file_by_version(
            bucket_name=bucket_name,
            file_name=file_name,
            file_ext=file_ext,
            version=version)

    def create_bucket(self,
                      bucket_name: str,
                      folder_name: str) -> None:
        """ Create a folder within an S3 Bucket

        Args:
            bucket_name (str): the bucket name (pre-exists)
            folder_name (str): the folder name (to be created)
        """

        self._create_folder(bucket_name=bucket_name,
                            folder_name=folder_name)

    def upload_images(self,
                      bucket_name: str,
                      folder_name: str,
                      file_paths: List[str]) -> None:
        """ Create a folder within an S3 Bucket

        Args:
            bucket_name (str): the bucket name (pre-exists)
            folder_name (str): the folder name (to be created)
            file_paths (List[str]): a list of fully qualified file paths
        """

        self._upload_images(bucket_name=bucket_name,
                            folder_name=folder_name,
                            file_paths=file_paths)
