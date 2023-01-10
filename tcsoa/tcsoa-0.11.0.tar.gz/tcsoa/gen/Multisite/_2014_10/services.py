from __future__ import annotations

from typing import List
from tcsoa.gen.Multisite._2014_10.ImportExportTCXML import RemoteImportResponse, RemoteExportResponse, RemoteImportUIDInfo, RemoteExportInfo, RemoteImportInfo
from tcsoa.base import TcService


class ImportExportTCXMLService(TcService):

    @classmethod
    def remoteExport(cls, rinfos: List[RemoteExportInfo]) -> RemoteExportResponse:
        """
        This operation exports targeted objects from the local site to the target sites using the Multi-Site TCXML
        payload. The target objects are specified in the RemoteExportInfo structure. The options also specified in this
        structure affect the final state of the exported objects at the target sites. The objects must be owned at the
        local site. 
        
        Use cases:
        In the Multi-Site federation user can share the business objects among the participating sites, the client
        shares business object(s) using the remote import or remote export functionality. This operation supports the
        following use case.
        The remote export (i.e. push) of business objects owned at the local site to the target site. The business
        object will exist at the target site either a replica or local object depending on options at the conclusion of
        the operation.
        """
        return cls.execute_soa_method(
            method_name='remoteExport',
            library='Multisite',
            service_date='2014_10',
            service_name='ImportExportTCXML',
            params={'rinfos': rinfos},
            response_cls=RemoteExportResponse,
        )

    @classmethod
    def remoteImport(cls, rinfos: List[RemoteImportInfo]) -> RemoteImportResponse:
        """
        The remoteImport operation imports targeted objects from their source site to the local site using the
        Multi-Site TCXML payload. The inputs include various options which will affect the final state of the Business
        Objects at the local site.
        
        Use cases:
        In the Multi-Site federation user can share the business objects among the participating sites, the client
        shares business object(s) using the remote import or remote export functionality. This operation supports the
        following use case.
        The remote import (i.e. pull) of business objects owned at the target site to the local site. The business
        object will exist at the local site as either a replica or local object depending on options at the conclusion
        of the operation. They will be updated if they already exist in the local site.
        """
        return cls.execute_soa_method(
            method_name='remoteImport',
            library='Multisite',
            service_date='2014_10',
            service_name='ImportExportTCXML',
            params={'rinfos': rinfos},
            response_cls=RemoteImportResponse,
        )

    @classmethod
    def remoteImportByUID(cls, rinfos: List[RemoteImportUIDInfo]) -> RemoteImportResponse:
        """
        The remoteImport operation imports targeted objects from their source site to the local site using the
        Multi-Site TCXML payload. The inputs include various options which will affect the final state of the Business
        Objects at the local site.
        
        Use cases:
        In the Multi-Site federation user can share the business objects among the participating sites, the client
        shares business object(s) using the remote import or remote export functionality. This operation supports the
        following use case.
        The remote import (i.e. pull) of business objects owned at the target site to the local site. The business
        object will exist at the local site as either a replica or local object depending on options at the conclusion
        of the operation. They will be updated if they already exist in the local site.
        """
        return cls.execute_soa_method(
            method_name='remoteImportByUID',
            library='Multisite',
            service_date='2014_10',
            service_name='ImportExportTCXML',
            params={'rinfos': rinfos},
            response_cls=RemoteImportResponse,
        )
