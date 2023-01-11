from __future__ import annotations

from tcsoa.gen.Internal.Administration._2017_11.IRM import AccessorsInfoResponse
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.base import TcService


class IRMService(TcService):

    @classmethod
    def getAccessorsInfo(cls, accessorObjects: List[BusinessObject]) -> AccessorsInfoResponse:
        """
        This operation can be used to get the name and type of the given accessor object. This name and type
        information is used by the Access Manager application to populate the accessors on the Access Control List.
        
        Use cases:
        Clients like RAC call this operation to get the name and type of the accessors. Access Manager application in
        RAC have a tabular representation of the accessors. Using this table user can grant or revoke the access for a
        particular privilege against a particular accessor. To render each such accessor on this Access Control List
        table RAC UI needs information like accessor name and accessor type. This information will be required for each
        accessor specified on the table. This operation will be used to get this information in bulk and render on the
        UI through UI component.
        """
        return cls.execute_soa_method(
            method_name='getAccessorsInfo',
            library='Internal-Administration',
            service_date='2017_11',
            service_name='IRM',
            params={'accessorObjects': accessorObjects},
            response_cls=AccessorsInfoResponse,
        )
