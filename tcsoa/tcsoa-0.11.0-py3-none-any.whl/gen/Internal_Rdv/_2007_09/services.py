from __future__ import annotations

from tcsoa.gen.Internal.Rdv._2007_09.VariantManagement import GetVariantExprAllDataResponse
from typing import List
from tcsoa.gen.BusinessObjects import NamedVariantExpression
from tcsoa.base import TcService


class VariantManagementService(TcService):

    @classmethod
    def getVariantExprXOChartData(cls, inputs: List[NamedVariantExpression]) -> GetVariantExprAllDataResponse:
        """
        This operation creates the necessary data required to display the Named Variant Expressions (NVEs) in the XO
        mode. inputs parameter contains the list of NVE references for which XO chart data is required. XO mode is an
        alternate way to display the Named Variant Expression.  In XO mode X means true and O means false.
        
        Use cases:
        This operation is called when there is a need to fetch the XO chart of the NVEs. This operation takes the list
        of NVE objects and returns the 'GetVariantExprAllDataResponse' object which contains the data required to
        create the XO chart and 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='getVariantExprXOChartData',
            library='Internal-Rdv',
            service_date='2007_09',
            service_name='VariantManagement',
            params={'inputs': inputs},
            response_cls=GetVariantExprAllDataResponse,
        )
