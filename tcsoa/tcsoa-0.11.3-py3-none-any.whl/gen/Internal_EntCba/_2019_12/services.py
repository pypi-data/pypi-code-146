from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.EntCba._2019_12.Alignments import PartDesOccAlignmentData
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class AlignmentsService(TcService):

    @classmethod
    def alignOccurrences(cls, input: List[PartDesOccAlignmentData]) -> ServiceData:
        """
        This operation aligns the Part and the Design occurrences. If the Part or the Design context is given, the
        alignment is performed using the provided context.  If no context is provided either for the Part occurrence or
        the Design occurrence, alignment is performed with the immediate parent occurrence as the context.
        """
        return cls.execute_soa_method(
            method_name='alignOccurrences',
            library='Internal-EntCba',
            service_date='2019_12',
            service_name='Alignments',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def unalignOccurrences(cls, input: List[PartDesOccAlignmentData]) -> ServiceData:
        """
        This operation unaligns the Part and the Design occurrences. If the Part or the Design context is given, the
        unalignment is performed using the provided context. If no context is provided either for the Part occurrence
        or Design occurrence, unalignment is performed with the immediate parent occurrence as the context.
        """
        return cls.execute_soa_method(
            method_name='unalignOccurrences',
            library='Internal-EntCba',
            service_date='2019_12',
            service_name='Alignments',
            params={'input': input},
            response_cls=ServiceData,
        )
