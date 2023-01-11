from abc import ABC
from abc import abstractmethod

from truera.protobuf.public.data_service import data_service_pb2 as ds_pb


class DataServiceCommunicator(ABC):

    @abstractmethod
    def put_secret_cred(
        self,
        req: ds_pb.PutCredentialRequest,
        request_context=None
    ) -> ds_pb.PutCredentialResponse:
        pass

    @abstractmethod
    def get_credential_metadata(
        self,
        req: ds_pb.GetCredentialMetadataRequest,
        request_context=None
    ) -> ds_pb.GetCredentialMetadataResponse:
        pass

    @abstractmethod
    def delete_credential(
        self,
        req: ds_pb.DeleteCredentialRequest,
        request_context=None
    ) -> ds_pb.DeleteCredentialResponse:
        pass

    @abstractmethod
    def load_data_source(
        self,
        req: ds_pb.LoadDataRequest,
        request_context=None
    ) -> ds_pb.RowsetStatusResponse:
        pass

    @abstractmethod
    def get_rowset_status(
        self,
        req: ds_pb.GetRowsetStatusRequest,
        request_context=None
    ) -> ds_pb.RowsetStatusResponse:
        pass

    @abstractmethod
    def get_rowset_metadata(
        self,
        req: ds_pb.GetRowsetMetadataRequest,
        request_context=None
    ) -> ds_pb.GetRowsetMetadataResponse:
        pass

    @abstractmethod
    def get_columns(
        self,
        req: ds_pb.GetRowsetColumnsRequest,
        request_context=None
    ) -> ds_pb.GetRowsetColumnsRequestResponse:
        pass

    @abstractmethod
    def apply_filter_to_rowset(
        self,
        req: ds_pb.ApplyFilterRequest,
        request_context=None
    ) -> ds_pb.RowsetResponse:
        pass

    @abstractmethod
    def join_rowsets(
        self,
        req: ds_pb.JoinRequest,
        request_context=None
    ) -> ds_pb.RowsetResponse:
        pass

    @abstractmethod
    def get_rows(
        self,
        req: ds_pb.GetRowsRequest,
        request_context=None
    ) -> ds_pb.GetRowsResponse:
        pass

    @abstractmethod
    def delete_rowset(
        self,
        req: ds_pb.DeleteRowsetRequest,
        request_context=None
    ) -> ds_pb.DeleteRowsetResponse:
        pass

    @abstractmethod
    def materialize_data(
        self,
        req: ds_pb.MaterializeDataRequest,
        request_context=None
    ) -> ds_pb.MaterializeDataResponse:
        pass

    @abstractmethod
    def get_materialize_data_status(
        self,
        req: ds_pb.GetMaterializeDataStatusRequest,
        request_context=None
    ) -> ds_pb.MaterializeDataResponse:
        pass

    @abstractmethod
    def delete_materialize_operation(
        self,
        req: ds_pb.DeleteMaterializeOperationRequest,
        request_context=None
    ) -> ds_pb.DeleteMaterializeOperationResponse:
        pass

    @abstractmethod
    def get_credentials(
        self,
        req: ds_pb.GetCredentialsRequest,
        request_context=None
    ) -> ds_pb.GetCredentialsResponse:
        pass

    @abstractmethod
    def get_rowsets(
        self,
        req: ds_pb.GetRowsetsRequest,
        request_context=None
    ) -> ds_pb.GetRowsetsResponse:
        pass

    @abstractmethod
    def get_materialize_operations(
        self,
        req: ds_pb.GetMaterializeOperationsRequest,
        request_context=None
    ) -> ds_pb.GetMaterializeOperationsResponse:
        pass

    @abstractmethod
    def register_schema(
        self,
        req: ds_pb.RegisterSchemaRequest,
        request_context=None
    ) -> ds_pb.RegisterSchemaResponse:
        pass

    @abstractmethod
    def get_schema(
        self,
        req: ds_pb.GetSchemaRequest,
        request_context=None
    ) -> ds_pb.GetSchemaResponse:
        pass

    @abstractmethod
    def delete_schema(
        self,
        req: ds_pb.DeleteSchemaRequest,
        request_context=None
    ) -> ds_pb.DeleteSchemaResponse:
        pass

    @abstractmethod
    def start_streaming_ingestion(
        self,
        req: ds_pb.StartStreamingIngestionRequest,
        request_context=None
    ) -> ds_pb.StartStreamingIngestionResponse:
        pass

    @abstractmethod
    def get_streaming_ingestion_status(
        self,
        req: ds_pb.GetStreamingIngestionStatusRequest,
        request_context=None
    ) -> ds_pb.GetStreamingIngestionStatusResponse:
        pass

    @abstractmethod
    def stop_streaming_ingestion(
        self,
        req: ds_pb.StopStreamingIngestionRequest,
        request_context=None
    ) -> ds_pb.StopStreamingIngestionResponse:
        pass
