from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.Cad._2008_05.DataManagement import ResolveAttrMappingsForNXResponse
from tcsoa.gen.Cad._2008_03.DataManagement import ResolveAttrMappingsInfo
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def resolveAttrMappingsForNX(cls, info: List[ResolveAttrMappingsInfo]) -> ResolveAttrMappingsForNXResponse:
        """
        Retrieves NX specific CAD attribute mapped properties for one or more datasets. Information includes whether
        the property is frozen in the NX semantic. Also, an attribute can be a preference or constant, these may also
        be frozen. The client will have to look in the returned list to determine which one contains the property. The
        expected order of processing from the client is to iterate through the input list of 'clientIds'. If 'clientId'
        is present in the 'resolvedMappingsMap', then process the corresponding 'MappedDatasetAttrPropertyInfo'. If it
        is not in the 'resolvedMappingsMap', check if the 'clientId' is present in the
        'resolvedConstOrPrefAttrInfoMap'. If the attribute mapping is of the ATTRMAP_preference or ATTRMAP_constant
        type, the mapped value may be found in the 'resolvedConstOrPrefAttrInfoMap'.
        
        Use cases:
        NX Client needs to know if an attribute is mapped and if mapped if it modifiable.
        """
        return cls.execute_soa_method(
            method_name='resolveAttrMappingsForNX',
            library='Internal-Cad',
            service_date='2008_05',
            service_name='DataManagement',
            params={'info': info},
            response_cls=ResolveAttrMappingsForNXResponse,
        )
