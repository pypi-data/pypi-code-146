from abc import ABC
from abc import abstractmethod

from truera.protobuf.public.scheduled_ingestion_service import \
    scheduled_ingestion_service_pb2 as periodic_pb


class ScheduledIngestionServiceCommunicator(ABC):

    @abstractmethod
    def schedule_ingestion(
        self, req: periodic_pb.ScheduleIngestionRequest
    ) -> periodic_pb.ScheduleIngestionResponse:
        pass

    @abstractmethod
    def get_schedule(
        self, req: periodic_pb.GetScheduleRequest
    ) -> periodic_pb.GetScheduleResponse:
        pass

    @abstractmethod
    def get_workflows(
        self, req: periodic_pb.GetWorkflowsRequest
    ) -> periodic_pb.GetWorkflowsResponse:
        pass

    @abstractmethod
    def cancel_workflow(
        self, req: periodic_pb.CancelWorkflowRequest
    ) -> periodic_pb.CancelWorkflowResponse:
        pass

    @abstractmethod
    def run_single_ingestion(
        self, req: periodic_pb.RunSingleIngestionRequest
    ) -> periodic_pb.RunSingleIngestionResponse:
        pass

    @abstractmethod
    def run_single_ingestion_sync(
        self, req: periodic_pb.RunSingleIngestionSyncRequest
    ) -> periodic_pb.RunSingleIngestionSyncResponse:
        pass

    @abstractmethod
    def get_run_status(
        self, req: periodic_pb.GetRunStatusRequest
    ) -> periodic_pb.GetRunStatusResponse:
        pass

    @abstractmethod
    def close(self):
        pass
