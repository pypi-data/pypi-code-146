from abc import ABC
from abc import abstractmethod
import logging
from typing import Iterator, Union

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.bad_data_communicator import \
    BadDataCommunicator
from truera.client.public.communicator.http_communicator import \
    HttpCommunicator
from truera.protobuf.dataquality import bad_data_service_pb2 as bd_pb


class HttpBadDataCommunicator(BadDataCommunicator):

    def __init__(
        self,
        connection_string: str,
        auth_details: AuthDetails,
        logger: logging.Logger,
        *,
        verify_cert: Union[bool, str] = True
    ):
        connection_str = connection_string.rstrip("/")
        self.connection_string = f"{connection_str}/api/baddata"
        self.http_communcatior = HttpCommunicator(
            connection_string=self.connection_string,
            auth_details=auth_details,
            logger=logger,
            verify_cert=verify_cert
        )
        self.http_communcatior.__not_supported_message = "RPC not supported via HTTP client"

    def get_schema_mismatch_rows(
        self, req: bd_pb.GetSchemaMismatchRowsRequest
    ) -> bd_pb.GetSchemaMismatchRowsResponse:
        uri = f"{self.connection_string}/schemamismatch/rows"
        json_req = self.http_communcatior._proto_to_json(req)
        json_resp = self.http_communcatior.get_request(uri, json_req)
        return self.http_communcatior._json_to_proto(
            json_resp, bd_pb.GetSchemaMismatchRowsResponse()
        )

    def get_schema_mismatch_row_stats(
        self, req: bd_pb.GetSchemaMismatchRowStatsRequest
    ) -> bd_pb.GetSchemaMismatchRowStatsResponse:
        uri = f"{self.connection_string}/schemamismatch/stats"
        json_req = self.http_communcatior._proto_to_json(req)
        json_resp = self.http_communcatior.get_request(uri, json_req)
        return self.http_communcatior._json_to_proto(
            json_resp, bd_pb.GetSchemaMismatchRowStatsResponse()
        )
