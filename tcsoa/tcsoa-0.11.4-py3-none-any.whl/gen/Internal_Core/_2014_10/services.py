from __future__ import annotations

from tcsoa.gen.Internal.Core._2014_10.FileManagement import GetPlmdFileTicketResponse, DatashareManagerDownloadInfo, DatashareManagerUploadInfo
from tcsoa.gen.BusinessObjects import ImanFile
from tcsoa.gen.Internal.Core._2014_10.Licensing import LicenseServerInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class FileManagementService(TcService):

    @classmethod
    def postCleanUpFileCommits(cls, files: List[ImanFile]) -> ServiceData:
        """
        This operation recommits the file  after it has been cleaned out from local volume by the File Management
        System (FMS) StoreAndForward feature. This operation is intended for use only by the DatabaseOperations()
        method of an FMSTransferTool transfer task running in a Dispatcher Client context.
        The File Management System (FMS) StoreAndForward feature redirects uploads to a temporary volume that is close
        to the uploading user, called a Default Local Volume. The system then transfers the file to its final home in a
        Default Volume in a background FMSTransferTool process executed on a Dispatcher Module.
        The first step of the background operation is to copy the file(s) from the Default Local Volume to the Default
        Volume and  commit the new volumes of each file to the Teamcenter database. The second step of the background
        operation is to clean up the files from local volume. Finally the task invokes this operation to re-commit the
        destination volume to null for each file to the Teamcenter database.
        This operation is unpublished.  It is supported only for internal Siemens PLM purposes.  Customers should not
        invoke this operation.
        """
        return cls.execute_soa_method(
            method_name='postCleanUpFileCommits',
            library='Internal-Core',
            service_date='2014_10',
            service_name='FileManagement',
            params={'files': files},
            response_cls=ServiceData,
        )

    @classmethod
    def getPlmdFileTicketForDownload(cls, infos: List[DatashareManagerDownloadInfo]) -> GetPlmdFileTicketResponse:
        """
        The operation generates a File Management System (FMS) transient read ticket for Product Lifecycle Management
        Data (PLMD) file. The PLMD file is used by Data Share Manager Application to asynchronously download the files
        from a Teamcenter volume to a local client environment. The PLMD file contains details like FMS Bootstrap URLs,
        dataset names, type, reference names, original file names, and absolute file paths and read tickets.
        This operation is unpublished.  It is supported only for internal Siemens PLM purposes.  Customers should not
        invoke this operation.
        """
        return cls.execute_soa_method(
            method_name='getPlmdFileTicketForDownload',
            library='Internal-Core',
            service_date='2014_10',
            service_name='FileManagement',
            params={'infos': infos},
            response_cls=GetPlmdFileTicketResponse,
        )

    @classmethod
    def getPlmdFileTicketForUpload(cls, infos: List[DatashareManagerUploadInfo]) -> GetPlmdFileTicketResponse:
        """
        The operation generates a File Management System (FMS) transient read ticket for Product Lifecycle Management
        Data (PLMD) file. The PLMD file is used by Data Share Manager Application to asynchronously upload the files
        from a  local client environment into a Teamcenter volume. The PLMD file contains details like FMS Bootstrap
        URLs, dataset names, type, reference names, original file names, and absolute file paths and read tickets.
        This operation is unpublished.  It is supported only for internal Siemens PLM purposes.  Customers should not
        invoke this operation.
        """
        return cls.execute_soa_method(
            method_name='getPlmdFileTicketForUpload',
            library='Internal-Core',
            service_date='2014_10',
            service_name='FileManagement',
            params={'infos': infos},
            response_cls=GetPlmdFileTicketResponse,
        )


class LicensingService(TcService):

    @classmethod
    def updateLicenseServer(cls, inputObjects: List[LicenseServerInput]) -> ServiceData:
        """
        This operation modifies the Fnd0LicenseServer business object for each 'LicenseServerInput' supplied. The
        'LicenseServerInput' structure contains information for properties such as license server name, host, port,
        protocol and failover servers, for a given license server.  A license server location is defined by its host
        and port.  It is not allowed to have two license server names pointing to the same license server location. The
        user performing the operation needs administrator privileges.
        """
        return cls.execute_soa_method(
            method_name='updateLicenseServer',
            library='Internal-Core',
            service_date='2014_10',
            service_name='Licensing',
            params={'inputObjects': inputObjects},
            response_cls=ServiceData,
        )
