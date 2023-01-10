from __future__ import annotations

from tcsoa.gen.Cad._2011_06.DataManagement import GetAllAttrMappingsResponse
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def getAllAttrMappings2(cls) -> GetAllAttrMappingsResponse:
        """
        This operation retrieves all CAD attribute mapping definitions. If a 'CadAttributeMappingDefinition' object has
        a path that includes a Generic Relationship Manager (GRM) or named reference part, the associated property
        descriptor and any attached 'ListOfValues' (LOV) objects will be returned. This operation also returns LOV
        attachments category information to be used in object based conditions.
        
        Since this operation returns existing Teamcenter attribute mappings, please reference the Teamcenter help
        section on creating attribute mappings.
        
        
        Use cases:
        User needs to have attributes set on an object in Teamcenter.
        
        For this operation, the client application uses the list of returned attribute mapping definitions to present
        the correct CAD attributes to the user that correspond to the correct Teamcenter attributes including property
        descriptor information about the Teamcenter attributes.
        
        
        Exceptions:
        >Service Exception    Thrown if any Teamcenter subsystem errors occur during the retrieval of all attribute
        mappings, finding the dataset type or finding the attribute mapping type.
        """
        return cls.execute_soa_method(
            method_name='getAllAttrMappings2',
            library='Cad',
            service_date='2011_06',
            service_name='DataManagement',
            params={},
            response_cls=GetAllAttrMappingsResponse,
        )
