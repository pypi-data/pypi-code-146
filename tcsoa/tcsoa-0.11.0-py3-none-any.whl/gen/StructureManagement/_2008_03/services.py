from __future__ import annotations

from tcsoa.gen.StructureManagement._2008_03.Composition import AssignChildLinesResponse, AssignChildLinesParameter
from typing import List
from tcsoa.base import TcService


class CompositionService(TcService):

    @classmethod
    def assignChildLines(cls, input: List[AssignChildLinesParameter]) -> AssignChildLinesResponse:
        """
        Assign lines from one or more parent to a new parent line.
        """
        return cls.execute_soa_method(
            method_name='assignChildLines',
            library='StructureManagement',
            service_date='2008_03',
            service_name='Composition',
            params={'input': input},
            response_cls=AssignChildLinesResponse,
        )
