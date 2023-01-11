from __future__ import annotations

from tcsoa.gen.BusinessObjects import Fnd0SecondaryAudit, Fnd0AuditLog
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetProcessHistoryAuditRecordsResponse(TcBaseObj):
    """
    Contains a list of  ProcessHistoryAuditRecordStruct structures (which contain process histroy audit record entry,
    chilren process histroy audit entries, audit record entries of secondary obeject associated with the process ) as
    well as a list of process names. Retrieved audit record entries will be added into standard ServiceData list of
    plain. Any failure will be returned in the ServiceData list of partial errors.
    
    :var processNames: Process names of multi process the given workspace object goes through.
    :var rootProcessHistoryAuditRecords: Root process histrory audit record entries for each process.
    :var serviceData: The service data.
    """
    processNames: List[str] = ()
    rootProcessHistoryAuditRecords: List[ProcessHistoryAuditRecordStruct] = ()
    serviceData: ServiceData = None


@dataclass
class ProcessHistoryAuditRecordStruct(TcBaseObj):
    """
    Contains one process histroy audit record entry and its children's audit records as well as secondary audit records
    of attachments/targets associated with it.
    
    :var auditRecord: One process history audit record entry of given workspace object.
    :var childrenAuditRecords: Children process history audit records of auditRecord.
    :var secondaryAuditRecords: Audit records of secondary obejct such as attachements/targets assoicated with the
    audit record (auditRecord)  of certain process.
    """
    auditRecord: Fnd0AuditLog = None
    childrenAuditRecords: List[ProcessHistoryAuditRecordStruct] = ()
    secondaryAuditRecords: List[Fnd0SecondaryAudit] = ()
