import logging
from typing import Union

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.backup_service_communicator import \
    BackupServiceCommunicator
from truera.client.public.communicator.http_communicator import \
    HttpCommunicator
from truera.protobuf.backup import backup_service_pb2 as backup_pb2


class HttpBackupServiceCommunicator(BackupServiceCommunicator):

    def __init__(
        self,
        connection_string: str,
        auth_details: AuthDetails,
        logger: logging.Logger,
        *,
        verify_cert: Union[bool, str] = True
    ):
        connection_string = connection_string.rstrip("/")
        self.connection_string = f"{connection_string}/api/backupservice/backup"
        self.http_communicator = HttpCommunicator(
            connection_string=self.connection_string,
            auth_details=auth_details,
            logger=logger,
            verify_cert=verify_cert
        )

    def trigger_backup(
        self,
        req: backup_pb2.TriggerBackupRequest,
        request_context=None
    ) -> backup_pb2.TriggerBackupResponse:
        uri = "{conn}/_trigger".format(conn=self.connection_string)
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, backup_pb2.TriggerBackupResponse()
        )

    def trigger_restore(
        self,
        req: backup_pb2.TriggerRestoreRequest,
        request_context=None
    ) -> backup_pb2.TriggerRestoreResponse:
        uri = "{conn}/_restore".format(conn=self.connection_string)
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, backup_pb2.TriggerRestoreResponse()
        )

    def list_backup(
        self,
        req: backup_pb2.ListBackupsRequest,
        request_context=None
    ) -> backup_pb2.ListBackupsRequest:
        uri = "{conn}".format(conn=self.connection_string)
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, backup_pb2.ListBackupsResponse()
        )

    def trigger_cleanup(
        self,
        req: backup_pb2.CleanupStaleBackupsRequest,
        request_context=None
    ) -> backup_pb2.CleanupStaleBackupsResponse:
        uri = "{conn}/_clean".format(conn=self.connection_string)
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, backup_pb2.CleanupStaleBackupsResponse()
        )
