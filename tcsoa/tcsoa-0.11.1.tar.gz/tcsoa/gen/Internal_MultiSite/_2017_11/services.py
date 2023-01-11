from __future__ import annotations

from tcsoa.gen.Internal.Multisite._2017_11.ArchiveRestore import ArchiveRestoreResponse, GetReportTicketResponse, NamesAndValues
from tcsoa.gen.BusinessObjects import BusinessObject, PublishedObject
from typing import List
from tcsoa.base import TcService


class ArchiveRestoreService(TcService):

    @classmethod
    def getReportFileTicket(cls, reportFileName: str) -> GetReportTicketResponse:
        """
        The operation generates a File Management System (FMS) transient read ticket for report file created by
        archive/restore background operation.
        
        Use cases:
        In the Multi-Site federation user can archive and restore  the business objects  in background mode using Rich
        Application Client. This frees up the RAC to do other tasks. A non-modal progress monitor gives frequent
        updates of the operation progress and  archive/restore operation completion report.
        """
        return cls.execute_soa_method(
            method_name='getReportFileTicket',
            library='Internal-Multisite',
            service_date='2017_11',
            service_name='ArchiveRestore',
            params={'reportFileName': reportFileName},
            response_cls=GetReportTicketResponse,
        )

    @classmethod
    def restoreObjects(cls, objects: List[PublishedObject], sessionOptionsAndValues: List[NamesAndValues]) -> ArchiveRestoreResponse:
        """
        This operation transfers the ownership of published objects representing the target objects  at archive site to
        the local site using the Multi-Site TCXML payload. Further it un-publishes the target objects at archive site
        and deletes the target object replicas at archive site. The options specified by NamesAndValues  structure
        affect the final state of the restored objects at the local sites.
        
        Use cases:
        In the Multi-Site federation user can restore the business objects by performing ownership transfer from
        archive site to local site.  After the successful ownership data transfer the replicated data in the archive
        site will be deleted.
        """
        return cls.execute_soa_method(
            method_name='restoreObjects',
            library='Internal-Multisite',
            service_date='2017_11',
            service_name='ArchiveRestore',
            params={'objects': objects, 'sessionOptionsAndValues': sessionOptionsAndValues},
            response_cls=ArchiveRestoreResponse,
        )

    @classmethod
    def archiveObjects(cls, objects: List[BusinessObject], excludeObjects: List[BusinessObject], sessionOptionsAndValues: List[NamesAndValues]) -> ArchiveRestoreResponse:
        """
        This operation transfers the ownership of  targeted objects from the local site to the archive site using the
        Multi-Site TCXML payload and publishes them at archive site. The target objects belonging to local site will 
        be archived. After the successful ownership data transfer the replicated data and published records in the
        participating sites in a Multi-Site federation will be deleted. The options specified by NamesAndValues
        structure affect the final state of the  archived objects at the target sites.
        
        Use cases:
        In the Multi-Site federation user can archive the business objects by performing ownership transfer to a remote
        site marked for archive purpose.  After the successful ownership data transfer the replicated data in the local
        site will be deleted.
        """
        return cls.execute_soa_method(
            method_name='archiveObjects',
            library='Internal-Multisite',
            service_date='2017_11',
            service_name='ArchiveRestore',
            params={'objects': objects, 'excludeObjects': excludeObjects, 'sessionOptionsAndValues': sessionOptionsAndValues},
            response_cls=ArchiveRestoreResponse,
        )
