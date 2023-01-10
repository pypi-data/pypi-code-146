from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.StructureManagement._2010_09.Structure import ReSequenceParameter
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class StructureService(TcService):

    @classmethod
    def resequence(cls, input: List[ReSequenceParameter]) -> ServiceData:
        """
        Re-Sequence the lines with start number and the increment number with option to re-sequence their number and
        ignoring Pert Flows.
        
        Use cases:
        User wants to re-sequence a 'WorkArea' structure, he invokes the operation with ignore flow flag, the structure
        will be re-sequenced.
        """
        return cls.execute_soa_method(
            method_name='resequence',
            library='Internal-StructureManagement',
            service_date='2010_09',
            service_name='Structure',
            params={'input': input},
            response_cls=ServiceData,
        )
