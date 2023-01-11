from __future__ import annotations

from tcsoa.gen.Internal.AuditManager._2012_09.ProcessHistoryManagement import GetProcessHistoryAuditRecordsResponse
from tcsoa.base import TcService
from tcsoa.gen.BusinessObjects import WorkspaceObject


class ProcessHistoryManagementService(TcService):

    @classmethod
    def getProcssHistoryAuditRecords(cls, wsoObject: WorkspaceObject) -> GetProcessHistoryAuditRecordsResponse:
        """
        Get process history audit records of given workspace object. One process usally contains multiple history audit
        records and one given workspace object may have multiply processes.
        """
        return cls.execute_soa_method(
            method_name='getProcssHistoryAuditRecords',
            library='Internal-AuditManager',
            service_date='2012_09',
            service_name='ProcessHistoryManagement',
            params={'wsoObject': wsoObject},
            response_cls=GetProcessHistoryAuditRecordsResponse,
        )
