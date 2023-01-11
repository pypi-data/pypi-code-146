from abc import ABC
from abc import abstractmethod
from typing import Generator, Iterator

from truera.protobuf.public import artifactrepo_pb2 as ar_pb


class ArtifactRepoCommunicator(ABC):

    @abstractmethod
    def ping(self, req: ar_pb.PingRequest) -> ar_pb.PingRequestResponse:
        pass

    @abstractmethod
    def put_resource(
        self,
        req: Generator[ar_pb.PutRequest, None, None],
        stream: bool = False
    ) -> ar_pb.PutRequestResponse:
        pass

    @abstractmethod
    def put_metadata(
        self, req: ar_pb.PutMetadataRequest
    ) -> ar_pb.PutMetadataRequestResponse:
        pass

    @abstractmethod
    def resource_exists(
        self, req: ar_pb.ExistsRequest
    ) -> ar_pb.ExistsRequestResponse:
        pass

    @abstractmethod
    def get_resource(
        self, req: ar_pb.GetRequest
    ) -> Iterator[ar_pb.GetRequestResponse]:
        pass

    @abstractmethod
    def get_metadata_for_entity(
        self, req: ar_pb.GetMetadataForEntityRequest
    ) -> ar_pb.GetMetadataForEntityRequestResponse:
        pass

    @abstractmethod
    def get_all_metadata_for_resource(
        self, req: ar_pb.GetAllMetadataRequest
    ) -> ar_pb.GetAllMetadataRequestResponse:
        pass

    @abstractmethod
    def delete_resource(self, req: ar_pb.DeleteRequest) -> None:
        pass

    @abstractmethod
    def delete_metadata(
        self, req: ar_pb.DeleteMetadataRequest
    ) -> ar_pb.DeleteMetadataRequestResponse:
        pass

    @abstractmethod
    def get_models(
        self, req: ar_pb.GetModelsRequest
    ) -> ar_pb.GetModelsResponse:
        pass

    @abstractmethod
    def get_splits(
        self, req: ar_pb.GetSplitsRequest
    ) -> ar_pb.GetSplitsResponse:
        pass
