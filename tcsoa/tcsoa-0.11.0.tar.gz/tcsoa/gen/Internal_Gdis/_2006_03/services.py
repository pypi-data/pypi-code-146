from __future__ import annotations

from tcsoa.gen.Internal.Gdis._2006_03.Reporting import PrecalRoutineInfoResponse
from tcsoa.base import TcService


class ReportingService(TcService):

    @classmethod
    def getPrecalRoutineInfo(cls, routineId: str, routineRev: str, fromDate: str, toDate: str, specSetCode: str) -> PrecalRoutineInfoResponse:
        """
        Get the percentage on target pre calculations for a given routine, date range and spec set code
        
        Exceptions:
        >- When not able to get pre-calculations data for given input
        
        """
        return cls.execute_soa_method(
            method_name='getPrecalRoutineInfo',
            library='Internal-Gdis',
            service_date='2006_03',
            service_name='Reporting',
            params={'routineId': routineId, 'routineRev': routineRev, 'fromDate': fromDate, 'toDate': toDate, 'specSetCode': specSetCode},
            response_cls=PrecalRoutineInfoResponse,
        )
