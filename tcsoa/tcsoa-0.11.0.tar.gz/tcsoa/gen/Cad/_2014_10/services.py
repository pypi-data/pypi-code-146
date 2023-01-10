from __future__ import annotations

from tcsoa.gen.Cad._2014_10.DataManagement import GetAttrMappingsFilter, GetAttrMappingsResponse
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def getAttrMappings(cls, filter: List[GetAttrMappingsFilter]) -> GetAttrMappingsResponse:
        """
        This operation retrieves all CAD attribute mapping definitions or only the definitions that match the dataset
        and item type combinations included in the input filter.  CadAttributeMappingDefinition objects are returned
        with the associated business object name and property descriptor name.  The business object name and property
        descriptor name can be used to get the 'PropertyDescription' object from the client-side Meta Model,
        'ClientMetaModel'.  The 'PropertyDescription' object can then be used to access any needed property descriptor
        information, such as attached 'ListOfValues' (LOV) objects.
        
        Since this operation returns existing Teamcenter attribute mappings, please reference the Teamcenter help
        section on creating attribute mappings.
        
        
        Use cases:
        User needs to have attributes set on an object in Teamcenter.
        
        For this operation, the client application uses the list of returned attribute mapping definitions to present
        the correct CAD attributes to the user that correspond to the correct Teamcenter attributes including property
        descriptor information about the Teamcenter attributes.
        
        
        Exceptions:
        >'Teamcenter::Soa::Server::ServiceException'
        
        Service Exception    Thrown if any Teamcenter subsystem errors occur during the retrieval of all attribute
        mappings, finding the dataset type or finding the attribute mapping type. 
        """
        return cls.execute_soa_method(
            method_name='getAttrMappings',
            library='Cad',
            service_date='2014_10',
            service_name='DataManagement',
            params={'filter': filter},
            response_cls=GetAttrMappingsResponse,
        )
