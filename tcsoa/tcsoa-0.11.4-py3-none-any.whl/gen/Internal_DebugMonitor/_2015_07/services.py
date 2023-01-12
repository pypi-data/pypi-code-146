from __future__ import annotations

from tcsoa.gen.Internal.DebugMonitor._2015_07.DebugLogging import PerformanceJournalLevelResponse
from tcsoa.base import TcService


class DebugLoggingService(TcService):

    @classmethod
    def setPerformanceJournalLevel(cls, level: int) -> bool:
        """
        Set the level of performance journaling
        
        Exceptions:
        >214610 The performance journaling level is invalid. Valid values are 0, 1, and 2.
        214611 The performance journaling level cannot be changed after journal entries have been written.
        """
        return cls.execute_soa_method(
            method_name='setPerformanceJournalLevel',
            library='Internal-DebugMonitor',
            service_date='2015_07',
            service_name='DebugLogging',
            params={'level': level},
            response_cls=bool,
        )

    @classmethod
    def getPerformanceJournalLevel(cls) -> PerformanceJournalLevelResponse:
        """
        Get the current level of performance journaling
        """
        return cls.execute_soa_method(
            method_name='getPerformanceJournalLevel',
            library='Internal-DebugMonitor',
            service_date='2015_07',
            service_name='DebugLogging',
            params={},
            response_cls=PerformanceJournalLevelResponse,
        )
