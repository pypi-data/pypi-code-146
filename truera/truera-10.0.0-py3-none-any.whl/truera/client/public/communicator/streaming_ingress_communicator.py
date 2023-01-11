from abc import ABC
from abc import abstractmethod

from truera.protobuf.public.streaming import \
    streaming_ingress_service_pb2 as si_pb


class StreamingIngressServiceCommunicator(ABC):

    @abstractmethod
    def ping(self, req: si_pb.PingRequest) -> si_pb.PingResponse:
        pass

    @abstractmethod
    def ingest_point(
        self, req: si_pb.IngestPointRequest
    ) -> si_pb.IngestPointResponse:
        pass

    @abstractmethod
    def ingest_bulk(
        self, req: si_pb.IngestBulkRequest
    ) -> si_pb.IngestBulkResponse:
        pass

    @abstractmethod
    def close(self):
        pass
