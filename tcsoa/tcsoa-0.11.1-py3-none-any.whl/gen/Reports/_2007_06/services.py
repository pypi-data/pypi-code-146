from __future__ import annotations

from tcsoa.gen.Reports._2007_06.CubeReports import ConstructReportURLResponse, TcRAReportsCriteria
from tcsoa.base import TcService


class CubeReportsService(TcService):

    @classmethod
    def constructReportURL(cls, inputCriteria: TcRAReportsCriteria) -> ConstructReportURLResponse:
        """
        Constructs the servlet URL required by clients to process the TcRA report definition operation (retrieve, view,
        edit, delete or set permission) specified. The report definition ID, context objects, message name is required
        to get this URL.
        
        Use cases:
        User retrieves/views/edits/deletes/sets permission for one TcRA report, this operation will generate the
        corresponding URL for the TcRA operation.
        """
        return cls.execute_soa_method(
            method_name='constructReportURL',
            library='Reports',
            service_date='2007_06',
            service_name='CubeReports',
            params={'inputCriteria': inputCriteria},
            response_cls=ConstructReportURLResponse,
        )
