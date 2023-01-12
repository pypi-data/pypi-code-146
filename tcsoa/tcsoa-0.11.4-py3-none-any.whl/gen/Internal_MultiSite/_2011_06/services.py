from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.Multisite._2011_06.ImportExportAsync import RemoteExportInfo
from tcsoa.base import TcService


class ImportExportAsyncService(TcService):

    @classmethod
    def remoteExport(cls, reInfos: List[RemoteExportInfo]) -> None:
        """
        The 'remoteExport' operation is used to export given business objects from the source site to the target site
        asynchronously. The export options supplied in the 'RemoteExportInfo' structure influences the business object
        export.  
        E.g. In case user supplies Include All revision as TRUE, from source site all versions of the dataset will be
        exported to target site.  
        
        When option(s) are not specified in the RemoteExportInfo structure, by default user session preferences at the
        exporting site are considered and default values are mentioned in the ImportExportOptionsInfo structure. 
        
        This operation is integrated with Multi-Site RPC framework and is callable only in Global Workflow based
        Multi-Site environment. Consequently no other clients can invoke this operation other than Global Workflow
        clients. This operation does not return any values.
        
        
        Use cases:
        - In the multisite federation, user can share the business objects among the participating sites. The client
        shares business object(s) using the remote import or remote export functionality. 
        - To remote export the business object, using the Rich Client (RAC), the source site user creates an item and
        exports it to the target site. At the target site, user performs local search with the item id. The local
        search should provide the item, which confirms the successful remote export. 
        - Also business object remote export can be achieved using the command line utility data_share f=send. 
        
        """
        return cls.execute_soa_method(
            method_name='remoteExport',
            library='Internal-Multisite',
            service_date='2011_06',
            service_name='ImportExportAsync',
            params={'reInfos': reInfos},
            response_cls=None,
        )
