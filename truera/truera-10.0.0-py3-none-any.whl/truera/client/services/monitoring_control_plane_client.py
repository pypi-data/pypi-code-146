import logging
from typing import Union

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.monitoring_control_plane_communicator import \
    MonitoringControlPlaneCommunicator
from truera.client.public.communicator.monitoring_control_plane_http_communicator import \
    HttpMonitoringControlPlaneCommunicator
from truera.protobuf.druid.ingestion_spec_pb2 import \
    IngestionSpec  # pylint: disable=no-name-in-module
from truera.protobuf.monitoring import \
    monitoring_control_plane_pb2 as sync_druid_pb


class MonitoringControlPlaneClient():

    def __init__(
        self,
        communicator: MonitoringControlPlaneCommunicator,
        logger=None
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
            communicator = HttpMonitoringControlPlaneCommunicator(
                connection_string,
                auth_details,
                logger,
                verify_cert=verify_cert
            )
        else:
            from truera.client.private.communicator.monitoring_control_plane_grpc_communicator import \
                GrpcMonitoringControlPlaneCommunicator
            communicator = GrpcMonitoringControlPlaneCommunicator(
                connection_string, auth_details, logger
            )
        return MonitoringControlPlaneClient(communicator, logger)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.communicator.close()

    def create_ingestion(self, spec: IngestionSpec, request_context=None):
        req = sync_druid_pb.CreateIngestionRequest(spec=spec)
        return self.communicator.create_ingestion(
            req, request_context=request_context
        )

    def list_druid_tables(self, project_id: str, request_context=None):
        req = sync_druid_pb.ListDruidTablesRequest(project_id=project_id)
        return self.communicator.list_druid_tables(
            req, request_context=request_context
        )
