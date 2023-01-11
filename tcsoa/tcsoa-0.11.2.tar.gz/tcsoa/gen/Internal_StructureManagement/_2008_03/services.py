from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.StructureManagement._2008_03.Structure import ReSequenceParameter
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class StructureService(TcService):

    @classmethod
    def resequence(cls, input: List[ReSequenceParameter]) -> ServiceData:
        """
        Re-Sequence the lines with the start number and the increment number with option to re-sequence their children
        by using predecessor relationship.
        
        Use cases:
        User has a large structure that has been restructured so that the find no values are not well organized. User
        invokes the operation to re-sequence the lines.
        
        """
        return cls.execute_soa_method(
            method_name='resequence',
            library='Internal-StructureManagement',
            service_date='2008_03',
            service_name='Structure',
            params={'input': input},
            response_cls=ServiceData,
        )
