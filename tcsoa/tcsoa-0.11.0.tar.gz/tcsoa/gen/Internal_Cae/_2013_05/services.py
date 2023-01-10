from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine
from tcsoa.gen.Internal.Cae._2013_05.StructureManagement import GetCAEPropertyComparisonDetailsResponse
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def getCAEPropertyComparisonDetails(cls, targetBomline: BOMLine) -> GetCAEPropertyComparisonDetailsResponse:
        """
        The attribute comparison in CAE Manager is performed by applying data mapping on the source BOMLine and
        comparing the attribute value resulting from data mapping with the attribute value of the source BOMLine using
        the Accountability Check framework.
        
        This operation retrieves details of the comparison for the provided BOMLine object after the user has executed
        the Accountability Check for attribute comparison in CAE Manager. These results can be displayed in the CAE
        Accountability Check results view or as an Excel report. 
        """
        return cls.execute_soa_method(
            method_name='getCAEPropertyComparisonDetails',
            library='Internal-Cae',
            service_date='2013_05',
            service_name='StructureManagement',
            params={'targetBomline': targetBomline},
            response_cls=GetCAEPropertyComparisonDetailsResponse,
        )
