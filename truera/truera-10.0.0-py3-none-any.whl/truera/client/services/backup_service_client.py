import logging
from typing import Union

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.backup_service_communicator import \
    BackupServiceCommunicator
from truera.client.public.communicator.backup_service_http_communicator import \
    HttpBackupServiceCommunicator
from truera.protobuf.backup import backup_service_pb2 as backup_pb


class BackupServiceClient():

    def __init__(
        self, communicator: BackupServiceCommunicator, logger=None
    ) -> None:
        self.logger = logger if logger else logging.getLogger(__name__)
        self.communicator = communicator

    @classmethod
    def create(
        cls,
        connection_string: str = None,
        logger=None,
        auth_details: AuthDetails = None,
        use_http: bool = False,
        *,
        verify_cert: Union[bool, str] = True
    ):
        if use_http:
            communicator = HttpBackupServiceCommunicator(
                connection_string,
                auth_details,
                logger,
                verify_cert=verify_cert
            )
        else:
            from truera.client.private.communicator.backup_service_grpc_communicator import \
                GrpcBackupServiceCommunicator
            communicator = GrpcBackupServiceCommunicator(
                connection_string, auth_details, logger
            )
        return BackupServiceClient(communicator, logger)

    def list_backup(self, request_context=None):
        req = backup_pb.ListBackupsRequest()
        response = self.communicator.list_backup(req, request_context)
        return response

    def trigger_cleanup(self, request_context=None):
        req = backup_pb.CleanupStaleBackupsRequest()
        response = self.communicator.trigger_cleanup(req, request_context)
        return response

    def trigger_backup(self, request_context=None):
        req = backup_pb.TriggerBackupRequest()
        response = self.communicator.trigger_backup(req, request_context)
        return response

    def trigger_restore(self, backup_path, request_context=None):
        req = backup_pb.TriggerRestoreRequest(backup_folder_path=backup_path)
        response = self.communicator.trigger_restore(req, request_context)
        return response
