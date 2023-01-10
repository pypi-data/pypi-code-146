from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.Integration._2008_06.IntegrationManagement import RenameIMFInfo
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class IntegrationManagementService(TcService):

    @classmethod
    def renameIMF(cls, infos: List[RenameIMFInfo]) -> ServiceData:
        """
        Sets the original file name on an input file object.
        """
        return cls.execute_soa_method(
            method_name='renameIMF',
            library='Internal-Integration',
            service_date='2008_06',
            service_name='IntegrationManagement',
            params={'infos': infos},
            response_cls=ServiceData,
        )
