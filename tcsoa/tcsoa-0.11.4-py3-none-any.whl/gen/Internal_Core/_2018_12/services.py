from __future__ import annotations

from tcsoa.gen.Internal.Core._2018_12.Licensing import LicenseServerInput2
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class LicensingService(TcService):

    @classmethod
    def updateLicenseServer2(cls, inputObjects: List[LicenseServerInput2]) -> ServiceData:
        """
        This operation modifies the 'Fnd0LicenseServer' business object for each 'LicenseServerInput2' supplied. The
        'LicenseServerInput2' structure contains information for properties such as license server name, host, port,
        type, protocol, failover servers and multiple servers for a given license server.  A license server location is
        defined by its host, port, and protocol.  It is not allowed to have two license server names pointing to the
        same license server location. The user performing the operation needs administrator privileges
        """
        return cls.execute_soa_method(
            method_name='updateLicenseServer2',
            library='Internal-Core',
            service_date='2018_12',
            service_name='Licensing',
            params={'inputObjects': inputObjects},
            response_cls=ServiceData,
        )
