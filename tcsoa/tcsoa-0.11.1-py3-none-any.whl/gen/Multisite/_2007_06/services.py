from __future__ import annotations

from typing import List
from tcsoa.gen.Multisite._2007_06.ImportExport import RemoteImportInfo
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ImportExportService(TcService):

    @classmethod
    def remoteImport(cls, infos: List[RemoteImportInfo]) -> ServiceData:
        """
        The 'remoteImport' operation is used to import given business objects from the target site to the source site.
        The import options supplied in the 'RemoteImportInfo' structure influences the business object import.
        
        E.g. In case user supplies 'Include All revision' as TRUE, from target site, source site will import all
        versions of the dataset.  
        
        When option(s) are not specified in the RemoteImportInfo structure, by default user session preferences at the
        importing site are considered for import.  Default values are mentioned under the 'RIAttributeInfo' structure.
        
        
        
        Use cases:
        - In the Multi-Site federation user can share the business objects among the participating sites, the client
        shares business object(s) using the remote import or remote export functionality. Incase of the remote import
        the source site need to publish the item to the object directory services. 
        - To remote import the business object, first the source site user creates an Item and publishes it to the
        default ODS. The target site user performs remote search with the item id and imports it to the target site
        using the remote import operation. On successful completion of remote import operation, the item is imported to
        the target site database.
        - Also remote import of business objects can be achieved using the command line utility data_share
        f=remote_import. 
        
        
        
        Exceptions:
        >.
        """
        return cls.execute_soa_method(
            method_name='remoteImport',
            library='Multisite',
            service_date='2007_06',
            service_name='ImportExport',
            params={'infos': infos},
            response_cls=ServiceData,
        )
