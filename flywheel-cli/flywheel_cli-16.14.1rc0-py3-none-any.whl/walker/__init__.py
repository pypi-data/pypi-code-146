"""Provides filesystem walkers"""
from .abstract_walker import AbstractWalker, FileInfo
from .azure_walker import AzureWalker
from .factory import create_archive_walker, create_walker
from .gcs_walker import GCSWalker
from .pyfs_walker import PyFsWalker
from .pyfs_zip_walker import PyFsZipWalker
from .s3_walker import S3Walker
from .s3_zip_walker import S3ZipWalker
