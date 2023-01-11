import logging
from typing import Union

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.data_service_communicator import \
    DataServiceCommunicator
from truera.client.public.communicator.http_communicator import \
    HttpCommunicator
from truera.protobuf.public.data_service import data_service_pb2 as ds_pb


class HttpDataServiceCommunicator(DataServiceCommunicator):

    def __init__(
        self,
        connection_string: str,
        auth_details: AuthDetails,
        logger: logging.Logger,
        *,
        verify_cert: Union[bool, str] = True
    ):
        connection_string = connection_string.rstrip("/")
        self.connection_string = f"{connection_string}/api/data/dataservice"
        self.http_communicator = HttpCommunicator(
            connection_string=self.connection_string,
            auth_details=auth_details,
            logger=logger,
            verify_cert=verify_cert
        )
        self.http_communicator.__not_supported_message = "RPC not supported via HTTP client"

    # Devnote: request_context is not used in the http case. The expectation today is that internal
    # calls will always use grpc and external calls will have a single channel which already has
    # request_context in it via interceptor.
    def get_columns(
        self,
        req: ds_pb.GetRowsetColumnsRequest,
        request_context=None
    ) -> ds_pb.GetRowsetColumnsRequestResponse:
        uri = "{conn}/{project_id}/Rowset/{rowset_id}/Columns".format(
            conn=self.connection_string,
            project_id=req.project_id,
            rowset_id=req.rowset_id
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.GetRowsetColumnsRequestResponse()
        )

    def get_rows(
        self,
        req: ds_pb.GetRowsRequest,
        request_context=None
    ) -> ds_pb.GetRowsResponse:
        uri = "{conn}/{project_id}/Rowset/{rowset_id}/Rows".format(
            conn=self.connection_string,
            project_id=req.project_id,
            rowset_id=req.rowset_id
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.GetRowsResponse()
        )

    def put_secret_cred(
        self,
        req: ds_pb.PutCredentialRequest,
        request_context=None
    ) -> ds_pb.PutCredentialResponse:
        uri = "{conn}/Credential".format(conn=self.connection_string)
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.put_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.PutCredentialResponse()
        )

    def get_credential_metadata(
        self, req, request_context=None
    ) -> ds_pb.GetCredentialMetadataResponse:
        uri = ""
        if req.id:
            uri = "{conn}/Credential/id/{id}".format(
                conn=self.connection_string, id=req.id
            )
        else:
            uri = "{conn}/Credential/name/{name}".format(
                conn=self.connection_string, name=req.name
            )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.GetCredentialMetadataResponse()
        )

    def delete_credential(
        self, req, request_context=None
    ) -> ds_pb.DeleteCredentialResponse:
        uri = "{conn}/Credential/{id_to_delete}".format(
            conn=self.connection_string, id_to_delete=req.id_to_delete
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.delete_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.DeleteCredentialResponse()
        )

    # Devnote: request_context is not used in the http case. The expectation today is that internal
    # calls will always use grpc and external calls will have a single channel which already has
    # request_context in it via interceptor.
    def load_data_source(
        self,
        req: ds_pb.LoadDataRequest,
        request_context=None
    ) -> ds_pb.RowsetStatusResponse:
        uri = f"{self.connection_string}/Rowset"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.RowsetStatusResponse()
        )

    # Devnote: request_context is not used in the http case. The expectation today is that internal
    # calls will always use grpc and external calls will have a single channel which already has
    # request_context in it via interceptor.
    def get_rowset_status(
        self,
        req: ds_pb.GetRowsetStatusRequest,
        request_context=None
    ) -> ds_pb.RowsetStatusResponse:
        uri = f"{self.connection_string}/{req.project_id}/Rowset/status"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.RowsetStatusResponse()
        )

    def get_rowset_metadata(
        self,
        req: ds_pb.GetRowsetMetadataRequest,
        request_context=None
    ) -> ds_pb.GetRowsetMetadataResponse:
        uri = f"{self.connection_string}/Rowset/{req.rowset_id}:metadata"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.GetRowsetMetadataResponse()
        )

    # Devnote: request_context is not used in the http case. The expectation today is that internal
    # calls will always use grpc and external calls will have a single channel which already has
    # request_context in it via interceptor.
    def apply_filter_to_rowset(
        self,
        req: ds_pb.ApplyFilterRequest,
        request_context=None
    ) -> ds_pb.RowsetResponse:
        uri = f"{self.connection_string}/{req.project_id}/Rowset/{req.rowset_id}:filter"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.RowsetResponse()
        )

    def join_rowsets(
        self,
        req: ds_pb.JoinRequest,
        request_context=None
    ) -> ds_pb.RowsetResponse:
        uri = "{conn}/Join".format(conn=self.connection_string)
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.RowsetResponse()
        )

    def delete_rowset(
        self,
        req: ds_pb.DeleteRowsetRequest,
        request_context=None
    ) -> ds_pb.DeleteRowsetResponse:
        uri = "{conn}/Rowset/{rowset_id}".format(
            conn=self.connection_string, rowset_id=req.rowset_id
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.delete_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.DeleteRowsetResponse()
        )

    # Devnote: request_context is not used in the http case. The expectation today is that internal
    # calls will always use grpc and external calls will have a single channel which already has
    # request_context in it via interceptor.
    def materialize_data(
        self,
        req: ds_pb.MaterializeDataRequest,
        request_context=None
    ) -> ds_pb.MaterializeDataResponse:
        uri = "{conn}/MaterializeOperation".format(conn=self.connection_string)
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.MaterializeDataResponse()
        )

    # Devnote: request_context is not used in the http case. The expectation today is that internal
    # calls will always use grpc and external calls will have a single channel which already has
    # request_context in it via interceptor.
    def get_materialize_data_status(
        self,
        req: ds_pb.GetMaterializeDataStatusRequest,
        request_context=None
    ) -> ds_pb.MaterializeDataResponse:
        uri = "{conn}/MaterializeOperation/{materialize_operation_id}/status".format(
            conn=self.connection_string,
            materialize_operation_id=req.materialize_operation_id
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.MaterializeDataResponse()
        )

    def delete_materialize_operation(
        self,
        req: ds_pb.DeleteMaterializeOperationRequest,
        request_context=None
    ) -> ds_pb.DeleteMaterializeOperationResponse:
        uri = "{conn}/dataservice/MaterializeOperation/{id_to_delete}".format(
            conn=self.connection_string,
            id_to_delete=req.materialize_operation_id
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.delete_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.DeleteMaterializeOperationResponse()
        )

    def get_credentials(
        self,
        req: ds_pb.GetCredentialsRequest,
        request_context=None
    ) -> ds_pb.GetCredentialsResponse:
        uri = f"{self.connection_string}/{req.project_id}/Credentials"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.GetCredentialsResponse()
        )

    def get_rowsets(
        self,
        req: ds_pb.GetRowsetsRequest,
        request_context=None
    ) -> ds_pb.GetRowsetsResponse:
        uri = f"{self.connection_string}/{req.project_id}/Rowsets"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.GetRowsetsResponse()
        )

    def get_materialize_operations(
        self,
        req: ds_pb.GetMaterializeOperationsRequest,
        request_context=None
    ) -> ds_pb.GetMaterializeOperationsResponse:
        uri = f"{self.connection_string}/{req.project_id}/MaterializeOperations"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.GetMaterializeOperationsResponse()
        )

    def close(self):
        self.http_communicator.close()

    def register_schema(
        self,
        req: ds_pb.RegisterSchemaRequest,
        request_context=None
    ) -> ds_pb.RegisterSchemaResponse:
        uri = f"{self.connection_string}/schema"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.RegisterSchemaResponse()
        )

    def get_schema(
        self,
        req: ds_pb.GetSchemaRequest,
        request_context=None
    ) -> ds_pb.GetSchemaResponse:
        uri = f"{self.connection_string}/schema/id/{req.schema_id}"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.GetSchemaResponse()
        )

    def delete_schema(
        self,
        req: ds_pb.DeleteSchemaRequest,
        request_context=None
    ) -> ds_pb.DeleteSchemaResponse:
        uri = f"{self.connection_string}/schema/id/{req.schema_id}"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.delete_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.DeleteSchemaResponse()
        )

    def start_streaming_ingestion(
        self,
        req: ds_pb.StartStreamingIngestionRequest,
        request_context=None
    ) -> ds_pb.StartStreamingIngestionResponse:
        uri = f"/dataservice/streaming/start/{req.input_topic_name}/{req.data_collection_id}"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.StartStreamingIngestionResponse()
        )

    def get_streaming_ingestion_status(
        self,
        req: ds_pb.GetStreamingIngestionStatusRequest,
        request_context=None
    ) -> ds_pb.GetStreamingIngestionStatusResponse:
        uri = f"/dataservice/streaming/status/{req.streaming_ingestion_id}"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.GetStreamingIngestionStatusResponse()
        )

    def stop_streaming_ingestion(
        self,
        req: ds_pb.StopStreamingIngestionRequest,
        request_context=None
    ) -> ds_pb.StopStreamingIngestionResponse:
        uri = f"/dataservice/streaming/shutdown"
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.delete_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, ds_pb.StopStreamingIngestionResponse()
        )
