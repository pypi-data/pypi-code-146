from abc import ABC
from abc import abstractmethod

from truera.protobuf.dataquality import bad_data_service_pb2 as bd_pb


class BadDataCommunicator(ABC):

    @abstractmethod
    def get_schema_mismatch_rows(
        self, req: bd_pb.GetSchemaMismatchRowsRequest
    ) -> bd_pb.GetSchemaMismatchRowsResponse:
        pass

    @abstractmethod
    def get_schema_mismatch_row_stats(
        self, req: bd_pb.GetSchemaMismatchRowStatsRequest
    ) -> bd_pb.GetSchemaMismatchRowStatsResponse:
        pass
