from abc import ABC
from abc import abstractmethod

from truera.protobuf.monitoring import \
    monitoring_control_plane_pb2 as sync_druid_pb


class MonitoringControlPlaneCommunicator(ABC):

    @abstractmethod
    def create_ingestion(
        self,
        req: sync_druid_pb.CreateIngestionRequest,
        request_context=None
    ) -> sync_druid_pb.CreateIngestionResponse:
        pass

    @abstractmethod
    def list_druid_tables(
        self,
        req: sync_druid_pb.ListDruidTablesRequest,
        request_context=None
    ) -> sync_druid_pb.ListDruidTablesResponse:
        pass
