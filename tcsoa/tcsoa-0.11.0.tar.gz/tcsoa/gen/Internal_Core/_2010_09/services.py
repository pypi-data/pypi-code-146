from __future__ import annotations

from tcsoa.gen.Internal.Core._2010_09.FileManagement import CommitReplacedFileInfo
from tcsoa.gen.Internal.Core._2010_09.DataManagement import DatasetFilesResponse, DatasetFileQueryInfo
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class FileManagementService(TcService):

    @classmethod
    def commitReplacedFiles(cls, commitInfos: List[CommitReplacedFileInfo], flags: List[bool]) -> ServiceData:
        """
        This operation is invoked after successfully uploading a file to a transient volume.
        These files are typically files which already exist in the Teamcenter volume.  It is not necessary that the
        files be attached to a Dataset as a named reference, though that is typical.   No Dataset or named reference
        relation is required or created during this operation.
        This operation will copy the file from its uploaded location in the transient volume into the filename
        specified in the regular Teamcenter volume.  If a new filename is specified, then the file will be moved to the
        new filename, and the previous file in the Teamcenter volume will be deleted.  If no new filename is specified,
        then the file will overwrite the original filename in the Teamcenter volume.
        This operation supports the replacement of a file in a Teamcenter volume.
        This operation is unpublished.  It is supported only for internal Siemens PLM purposes.  Customers should not
        invoke this operation.
        
        Use cases:
        This operation supports the use case of replacing files attached to an ImanFile object, in a Teamcenter
        transient volume.
        """
        return cls.execute_soa_method(
            method_name='commitReplacedFiles',
            library='Internal-Core',
            service_date='2010_09',
            service_name='FileManagement',
            params={'commitInfos': commitInfos, 'flags': flags},
            response_cls=ServiceData,
        )


class DataManagementService(TcService):

    @classmethod
    def getDatasetFiles(cls, inputs: List[DatasetFileQueryInfo], retrieveFiles: bool) -> DatasetFilesResponse:
        """
        This operation fetches the Dataset instances and files for the given query criteria.
        """
        return cls.execute_soa_method(
            method_name='getDatasetFiles',
            library='Internal-Core',
            service_date='2010_09',
            service_name='DataManagement',
            params={'inputs': inputs, 'retrieveFiles': retrieveFiles},
            response_cls=DatasetFilesResponse,
        )
