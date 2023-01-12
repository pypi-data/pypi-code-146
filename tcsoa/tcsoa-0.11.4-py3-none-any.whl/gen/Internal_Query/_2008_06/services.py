from __future__ import annotations

from tcsoa.gen.Internal.Query._2008_06.Finder import FindObjectsInput, FindObjectsResponse
from tcsoa.base import TcService


class FinderService(TcService):

    @classmethod
    def findObjectsByClassAndAttributes(cls, input: FindObjectsInput) -> FindObjectsResponse:
        """
        Returns a list of values or objects for a specific class type with certain attributes and values.
        
        Use cases:
        Search for objects using given class type, attribute names and values.
        """
        return cls.execute_soa_method(
            method_name='findObjectsByClassAndAttributes',
            library='Internal-Query',
            service_date='2008_06',
            service_name='Finder',
            params={'input': input},
            response_cls=FindObjectsResponse,
        )
