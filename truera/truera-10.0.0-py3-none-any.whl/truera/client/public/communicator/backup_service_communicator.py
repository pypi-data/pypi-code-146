from abc import ABC
from abc import abstractmethod

from truera.protobuf.backup import backup_service_pb2 as backup_pb2


class BackupServiceCommunicator(ABC):

    @abstractmethod
    def trigger_backup(
        self,
        req: backup_pb2.TriggerBackupRequest,
        request_context=None
    ) -> backup_pb2.TriggerBackupResponse:
        pass

    @abstractmethod
    def trigger_restore(
        self,
        req: backup_pb2.TriggerRestoreRequest,
        request_context=None
    ) -> backup_pb2.TriggerRestoreResponse:
        pass

    @abstractmethod
    def list_backup(
        self,
        req: backup_pb2.ListBackupsRequest,
        request_context=None
    ) -> backup_pb2.ListBackupsRequest:
        pass

    @abstractmethod
    def trigger_cleanup(
        self,
        req: backup_pb2.CleanupStaleBackupsRequest,
        request_context=None
    ) -> backup_pb2.CleanupStaleBackupsResponse:
        pass
