from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine
from tcsoa.gen.Rdv._2009_04.ContextManagement import GetPastePrimeInfo, GetGOPartSolutionsResponse
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ContextManagementService(TcService):

    @classmethod
    def getAllGOPartSolutions(cls, goBomLine: BOMLine) -> GetGOPartSolutionsResponse:
        """
        Get the required information for display of part solutions of selected GBE and its instantiating ABE
        """
        return cls.execute_soa_method(
            method_name='getAllGOPartSolutions',
            library='Rdv',
            service_date='2009_04',
            service_name='ContextManagement',
            params={'goBomLine': goBomLine},
            response_cls=GetGOPartSolutionsResponse,
        )

    @classmethod
    def getPastePrimeAttributes(cls, input: GetPastePrimeInfo) -> ServiceData:
        """
        This operation pastes source Architecture Breakdown Element (ABE) BOMLine to the target Architecture Breakdown
        (AB) BOMLine. It pastes all the parents (up to top level AB) of the source ABE under target AB. This operation
        also copies the variability, Named Variant Expressions (NVEs) and part solutions from the source BOMLine to
        target BOMLine.
        
        Use cases:
        This operation can be used to paste the source Architecture Breakdown Element BOMLine to target Architecture
        Breakdown BOMLine.
        
        Use case 1: Copy variability
        User needs to set flag value as 1 in GetPastePrimeInfo structure to copy only the variability from the source
        BOMLine to target BOMLine.
        
        Use case 2: Copy variability and NamedVariantExpressions
        User needs to set flag value as 2 in GetPastePrimeInfo structure to copy the variability and Named Variant
        Expressions from the source BOMLine to target BOMLine.
        
        Use case 3: Copy variability, NamedVariantExpressions and part solutions
        User needs to set flag value as 3 in GetPastePrimeInfo structure to copy the variability, Named Variant
        Expressions and part solutions from the source BOMLine to target BOMLine.
        """
        return cls.execute_soa_method(
            method_name='getPastePrimeAttributes',
            library='Rdv',
            service_date='2009_04',
            service_name='ContextManagement',
            params={'input': input},
            response_cls=ServiceData,
        )
