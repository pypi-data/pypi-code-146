from __future__ import annotations

from tcsoa.gen.Internal.DebugMonitor._2019_06.DebugLogging import Logflags, DebugLoggingResponse
from tcsoa.base import TcService


class DebugLoggingService(TcService):

    @classmethod
    def startLogging(cls, logFlags: Logflags) -> DebugLoggingResponse:
        """
        This operation enables logging of the debug log flags that are passed through logFlags.
        """
        return cls.execute_soa_method(
            method_name='startLogging',
            library='Internal-DebugMonitor',
            service_date='2019_06',
            service_name='DebugLogging',
            params={'logFlags': logFlags},
            response_cls=DebugLoggingResponse,
        )

    @classmethod
    def stopLogging(cls) -> DebugLoggingResponse:
        """
        This operation disables logging of the selected log type, collects all the generated log files and creates a
        zip file of the logs. It either returns a FMS transient file ticket of a zip file containg all the relavent log
        files, or a message informing the user to contact the system adminstrator for access to the zip file.
        """
        return cls.execute_soa_method(
            method_name='stopLogging',
            library='Internal-DebugMonitor',
            service_date='2019_06',
            service_name='DebugLogging',
            params={},
            response_cls=DebugLoggingResponse,
        )
