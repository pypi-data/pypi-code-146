from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.Administration._2009_10.PersonManagement import NameValueMap, GetPersonPropertiesResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class PersonManagementService(TcService):

    @classmethod
    def getStringProperties(cls, personObjects: List[BusinessObject], attributes: List[str]) -> GetPersonPropertiesResponse:
        """
        This operation retrieves the values of the given properties for the given Person business objects.  The
        supported property names are: locale and time zone. Other property names would be ignored if they are passed in.
        
        Use cases:
        Check the existing time zones or locales of Teamcenter users.
        """
        return cls.execute_soa_method(
            method_name='getStringProperties',
            library='Internal-Administration',
            service_date='2009_10',
            service_name='PersonManagement',
            params={'personObjects': personObjects, 'attributes': attributes},
            response_cls=GetPersonPropertiesResponse,
        )

    @classmethod
    def setStringProperties(cls, personObject: List[BusinessObject], attributes: NameValueMap) -> ServiceData:
        """
        This operation sets the values of the given properties for each Person business object passed in the given
        person object list. The property names specified in attributes map must be locale and timezone. Other
        properties would be ignored. The values of the given properties will be updated on all Person business objects
        given in the list.
        
        Use cases:
        Update locale and timezone properties of a set of Person business objects when those persons are relocated to
        different time zones or different countries
        """
        return cls.execute_soa_method(
            method_name='setStringProperties',
            library='Internal-Administration',
            service_date='2009_10',
            service_name='PersonManagement',
            params={'personObject': personObject, 'attributes': attributes},
            response_cls=ServiceData,
        )
