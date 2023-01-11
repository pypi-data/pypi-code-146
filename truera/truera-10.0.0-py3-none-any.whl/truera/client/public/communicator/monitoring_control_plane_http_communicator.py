import logging
from typing import Union

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.http_communicator import \
    HttpCommunicator
from truera.client.public.communicator.monitoring_control_plane_communicator import \
    MonitoringControlPlaneCommunicator
from truera.protobuf.monitoring import \
    monitoring_control_plane_pb2 as sync_druid_pb


class HttpMonitoringControlPlaneCommunicator(
    MonitoringControlPlaneCommunicator
):

    def __init__(
        self,
        connection_string: str,
        auth_details: AuthDetails,
        logger: logging.Logger,
        *,
        verify_cert: Union[bool, str] = True
    ):
        connection_string = connection_string.rstrip("/")
        self.connection_string = f"{connection_string}/api/monitoring"
        self.http_communicator = HttpCommunicator(
            connection_string=self.connection_string,
            auth_details=auth_details,
            logger=logger,
            verify_cert=verify_cert
        )

    def create_ingestion(
        self,
        req: sync_druid_pb.CreateIngestionRequest,
        request_context=None
    ) -> sync_druid_pb.CreateIngestionResponse:
        pass

    def list_druid_tables(
        self,
        req: sync_druid_pb.ListDruidTablesRequest,
        request_context=None
    ) -> sync_druid_pb.ListDruidTablesResponse:
        uri = "{conn}/druid-tables/{project_id}".format(
            conn=self.connection_string, project_id=req.project_id
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, sync_druid_pb.ListDruidTablesResponse()
        )
