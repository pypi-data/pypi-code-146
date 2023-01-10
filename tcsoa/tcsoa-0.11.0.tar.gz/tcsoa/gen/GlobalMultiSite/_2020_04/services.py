from __future__ import annotations

from tcsoa.gen.GlobalMultiSite._2020_04.ImportExport import ImportObjectsFromPLMXMLWithDSMResp
from tcsoa.gen.BusinessObjects import TransferMode, ItemRevision
from typing import List
from tcsoa.gen.GlobalMultiSite._2007_12.ImportExport import NamesAndValues
from tcsoa.base import TcService


class ImportExportService(TcService):

    @classmethod
    def importObjectsFromPLMXMLWithDSM(cls, xmlFileTicket: str, namedRefFolderPath: str, transfermode: TransferMode, icRev: ItemRevision, sessionOptions: List[NamesAndValues]) -> ImportObjectsFromPLMXMLWithDSMResp:
        """
        The operation imports the objects from a PLM XML file, and returns the .plmd file read tickets for the Dataset
        named reference files in the PLM XML file. The tickets are used to upload the files to FMS volume using Data
        Share Manager system. The PLM XML file must be uploaded to the transient volume before the calling of this
        operation.
        
        Use cases:
        Use Case 1: Import PLMXML file to database with Data Share Manager configured.
        User can import PLMXML file using the steps below:
        1)    Upload the XML file to the transient volume using the API getTransientFileTicketsForUpload from
        FileManagementService, API RegisterTickets and API uploadFilesToPlm from FmsFileCacheProxy.
        2)    Call the service operation importObjectsFromPLMXMLWithDSM by specifying the XML file ticket, the Dataset
        named reference files folder path, the export transfermode, the incremental change context, and session options
        as the input arguments.
        3)    Upload the Dataset named reference files to the FMS volume using the namedRefPLMDFileTickets in the
        returned ImportObjectsFromPLMXMLWithDSMResp as the input argument for API DownloadFilesWithDM from IFileManager.
        4)    Download the import log file using the logFileTicket in the returned ImportObjectsFromPLMXMLWithDSMResp
        and the API RegisterTicket and API DownLoadTransientFile from FmsFileCacheProxy.
        """
        return cls.execute_soa_method(
            method_name='importObjectsFromPLMXMLWithDSM',
            library='GlobalMultiSite',
            service_date='2020_04',
            service_name='ImportExport',
            params={'xmlFileTicket': xmlFileTicket, 'namedRefFolderPath': namedRefFolderPath, 'transfermode': transfermode, 'icRev': icRev, 'sessionOptions': sessionOptions},
            response_cls=ImportObjectsFromPLMXMLWithDSMResp,
        )
