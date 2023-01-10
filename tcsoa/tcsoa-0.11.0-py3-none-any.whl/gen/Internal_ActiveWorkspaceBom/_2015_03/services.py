from __future__ import annotations

from tcsoa.gen.Internal.ActiveWorkspaceBom._2015_03.OccurrenceManagement import AttachObjectsInputData, AttachObjectsResp
from typing import List
from tcsoa.base import TcService


class OccurrenceManagementService(TcService):

    @classmethod
    def attachObjects(cls, input: List[AttachObjectsInputData]) -> AttachObjectsResp:
        """
        This operation attaches the secondary object with the primary with the given relation. If the context is
        specified then secondary object is associated in-context.
        
        Use cases:
        User wants to attach an object with occurrence present in the product.
        """
        return cls.execute_soa_method(
            method_name='attachObjects',
            library='Internal-ActiveWorkspaceBom',
            service_date='2015_03',
            service_name='OccurrenceManagement',
            params={'input': input},
            response_cls=AttachObjectsResp,
        )
