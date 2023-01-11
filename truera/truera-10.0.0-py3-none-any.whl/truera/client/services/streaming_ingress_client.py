import logging
from typing import List, Union

from crontab import CronTab
from google.protobuf.json_format import Parse

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.streaming_ingress_communicator import \
    StreamingIngressServiceCommunicator
from truera.client.public.communicator.streaming_ingress_http_communicator import \
    HttpStreamingIngressServiceCommunicator
import truera.client.services.data_service_client as ds_client
from truera.protobuf.public.data_service import \
    data_service_messages_pb2 as ds_messages_pb
from truera.protobuf.public.data_service import data_service_pb2 as ds_pb
from truera.protobuf.public.streaming import \
    streaming_ingress_service_pb2 as si_pb


class StreamingIngressClient():

    def __init__(
        self,
        communicator: StreamingIngressServiceCommunicator,
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
            communicator = HttpStreamingIngressServiceCommunicator(
                connection_string,
                auth_details,
                logger,
                verify_cert=verify_cert
            )
        else:
            from truera.client.private.communicator.streaming_ingress_grpc_communicator import \
                GrpcStreamingIngressServiceCommunicator
            communicator = GrpcStreamingIngressServiceCommunicator(
                connection_string, auth_details, logger
            )
        return StreamingIngressClient(communicator, logger)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.communicator.close()

    def ping(self):
        return self.communicator.ping(si_pb.PingRequest())

    def ingest_point(
        self,
        project_id: str,
        data_collection_id: str,
        **kwargs,
    ):
        req = si_pb.IngestPointRequest(
            project_id=project_id,
            data_collection_id=data_collection_id,
            **kwargs,
        )
        return self.communicator.ingest_point(req)

    def ingest_bulk(
        self,
        project_id: str,
        data_collection_id: str,
        points: List[si_pb.BulkPoint],
        **kwargs,
    ):
        req = si_pb.IngestBulkRequest(
            project_id=project_id,
            data_collection_id=data_collection_id,
            points=points,
            **kwargs,
        )
        return self.communicator.ingest_bulk(req)
