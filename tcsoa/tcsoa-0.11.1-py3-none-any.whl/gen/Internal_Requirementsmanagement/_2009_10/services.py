from __future__ import annotations

from tcsoa.gen.Internal.Requirementsmanagement._2009_10.RequirementsManagement import ImportUnmanagedDataResponse, RelativeStructureParentInfo
from typing import List
from tcsoa.base import TcService


class RequirementsManagementService(TcService):

    @classmethod
    def importUnmanagedData(cls, relativeStructParent: List[RelativeStructureParentInfo], importOptions: List[str]) -> ImportUnmanagedDataResponse:
        """
        The SOA operation is used to create and update structures and GRM from MSExcel application. It provides ability
        to create or delete items, GRM and is capable of property editing.
        
        Use cases:
        Create and update item and GRM from exported Excel or from standalone excel sheet.
        
        Exceptions:
        >If the object is modified, New or Deleted from Teamcenter there is any error during generating transient file
        read ticket due to a configuration issue at the server, then the operation throws a service exception. Example-
        If the transient volume directory is not configured at the server then the FMS fails to generate a file at the
        server and subsequent file download operation fails. In such situation a service exception is thrown.
        """
        return cls.execute_soa_method(
            method_name='importUnmanagedData',
            library='Internal-Requirementsmanagement',
            service_date='2009_10',
            service_name='RequirementsManagement',
            params={'relativeStructParent': relativeStructParent, 'importOptions': importOptions},
            response_cls=ImportUnmanagedDataResponse,
        )
