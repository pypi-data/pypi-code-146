from __future__ import annotations

from tcsoa.gen.WProxy._2014_10.ProxyLink import CreateProxyLinkInputInfo
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ProxyLinkService(TcService):

    @classmethod
    def createProxyLink(cls, input: List[CreateProxyLinkInputInfo]) -> ServiceData:
        """
        This operation creates ProxyLink object(s) based on the input information provided and relates it to the
        primary objects at the proxy link site.
        
        Use cases:
        When the user wants to provide information about an object to a site other than the owning site of the object,
        the user can create a proxy link for that object.  From the different site, User can access the master object
        using the proxy link.
        """
        return cls.execute_soa_method(
            method_name='createProxyLink',
            library='WProxy',
            service_date='2014_10',
            service_name='ProxyLink',
            params={'input': input},
            response_cls=ServiceData,
        )
