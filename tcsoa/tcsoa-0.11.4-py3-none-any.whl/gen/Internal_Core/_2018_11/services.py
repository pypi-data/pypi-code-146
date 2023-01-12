from __future__ import annotations

from tcsoa.gen.Internal.Core._2018_11.LogicalObject import AddIncludedLogicalObjectsResponse, AddIncludedLOInput
from tcsoa.gen.Internal.Core._2018_11.FileManagement import GetTransientTicketsDownloadResponse, GetTransientTicketsDownloadInput
from typing import List
from tcsoa.base import TcService


class FileManagementService(TcService):

    @classmethod
    def getTransientFileTicketsForDownload(cls, tickets: List[GetTransientTicketsDownloadInput]) -> GetTransientTicketsDownloadResponse:
        """
        This operation obtains File Management System (FMS) transient file read tickets for the supplied transient file
        write tickets. Optionally it deletes the file from temporary storage if specified in input.
        
        Use cases:
        One SOA client want to send another SOA client a temporary file using the FMS system. The two clients already
        have means of communicating with each other without using SOA but want to use the FMS system for bulk
        transfers. 
        
        The client sending the file to the other client uses the following two  service operations:
        Teamcenter::Services::Core::FilemanagementService::getTransientFileTicketsForUpload to generate a write ticket
        for upload, followed by Teamcenter::Soa::Client::FccProxy::uploadFiles to upload the file using the write
        ticket.
        
        In order to give the other SOA client a read ticket for this uploaded file, a new ticket needs to be generated.
        The client sending the file then uses this operation getTransientFileTicketsForDownload to generate a read
        ticket for the file that was just uploaded.
        
        After the other SOA client receives this ticket, it uses the
        Teamcenter::Soa::Client::FccProxy::downloadFilesToLocation operation to download the file using the read ticket.
        """
        return cls.execute_soa_method(
            method_name='getTransientFileTicketsForDownload',
            library='Internal-Core',
            service_date='2018_11',
            service_name='FileManagement',
            params={'tickets': tickets},
            response_cls=GetTransientTicketsDownloadResponse,
        )


class LogicalObjectService(TcService):

    @classmethod
    def addIncludedLogicalObjects(cls, addIncludedLOInput: AddIncludedLOInput) -> AddIncludedLogicalObjectsResponse:
        """
        This operation adds other logical object types to an existing Logical Object Type based on the specified input.
        
        Use cases:
        This operation is invoked to add included logical objects to an existing Logical Object Type.
        """
        return cls.execute_soa_method(
            method_name='addIncludedLogicalObjects',
            library='Internal-Core',
            service_date='2018_11',
            service_name='LogicalObject',
            params={'addIncludedLOInput': addIncludedLOInput},
            response_cls=AddIncludedLogicalObjectsResponse,
        )
