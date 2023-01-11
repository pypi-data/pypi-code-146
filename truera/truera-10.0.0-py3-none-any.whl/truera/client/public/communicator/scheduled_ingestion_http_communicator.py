import logging
from typing import Union

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.http_communicator import \
    HttpCommunicator
from truera.client.public.communicator.scheduled_ingestion_communicator import \
    ScheduledIngestionServiceCommunicator
from truera.protobuf.public.scheduled_ingestion_service import \
    scheduled_ingestion_service_pb2 as periodic_pb


class HttpScheduledIngestionServiceCommunicator(
    ScheduledIngestionServiceCommunicator
):

    def __init__(
        self,
        connection_string: str,
        auth_details: AuthDetails,
        logger: logging.Logger,
        *,
        verify_cert: Union[bool, str] = True
    ):
        connection_string = connection_string.rstrip("/")
        self.connection_string = f"{connection_string}/api/data/scheduled_ingestion"
        self.http_communcatior = HttpCommunicator(
            connection_string=self.connection_string,
            auth_details=auth_details,
            logger=logger,
            verify_cert=verify_cert
        )
        self.http_communcatior.__not_supported_message = "RPC not supported via HTTP client"

    def schedule_ingestion(
        self, req: periodic_pb.ScheduleIngestionRequest
    ) -> periodic_pb.ScheduleIngestionResponse:
        uri = f"{self.connection_string}/schedule"
        json_req = self.http_communcatior._proto_to_json(req)
        json_resp = self.http_communcatior.post_request(uri, json_req)
        return self.http_communcatior._json_to_proto(
            json_resp, periodic_pb.ScheduleIngestionResponse()
        )

    def get_schedule(
        self, req: periodic_pb.GetScheduleRequest
    ) -> periodic_pb.GetScheduleResponse:
        uri = f"{self.connection_string}/schedule/{req.workflow_id}"
        json_req = self.http_communcatior._proto_to_json(req)
        json_resp = self.http_communcatior.get_request(uri, json_req)
        return self.http_communcatior._json_to_proto(
            json_resp, periodic_pb.GetScheduleResponse()
        )

    def get_workflows(
        self, req: periodic_pb.GetWorkflowsRequest
    ) -> periodic_pb.GetWorkflowsResponse:
        uri = f"{self.connection_string}/workflows/"
        json_req = self.http_communcatior._proto_to_json(req)
        json_resp = self.http_communcatior.get_request(uri, json_req)
        return self.http_communcatior._json_to_proto(
            json_resp, periodic_pb.GetWorkflowsResponse()
        )

    def cancel_workflow(
        self, req: periodic_pb.CancelWorkflowRequest
    ) -> periodic_pb.CancelWorkflowResponse:
        uri = f"{self.connection_string}/schedule/{req.workflow_id}"
        json_req = self.http_communcatior._proto_to_json(req)
        json_resp = self.http_communcatior.delete_request(uri, json_req)
        return self.http_communcatior._json_to_proto(
            json_resp, periodic_pb.CancelWorkflowResponse()
        )

    def run_single_ingestion(
        self, req: periodic_pb.RunSingleIngestionRequest
    ) -> periodic_pb.RunSingleIngestionResponse:
        uri = f"{self.connection_string}/run_single"
        json_req = self.http_communcatior._proto_to_json(req)
        json_resp = self.http_communcatior.post_request(uri, json_req)
        return self.http_communcatior._json_to_proto(
            json_resp, periodic_pb.RunSingleIngestionResponse()
        )

    def run_single_ingestion_sync(
        self, req: periodic_pb.RunSingleIngestionSyncRequest
    ) -> periodic_pb.RunSingleIngestionSyncResponse:
        uri = f"{self.connection_string}/run_single_sync"
        json_req = self.http_communcatior._proto_to_json(req)
        json_resp = self.http_communcatior.post_request(uri, json_req)
        return self.http_communcatior._json_to_proto(
            json_resp, periodic_pb.RunSingleIngestionSyncResponse()
        )

    def get_run_status(
        self, req: periodic_pb.GetRunStatusRequest
    ) -> periodic_pb.GetRunStatusResponse:
        uri = f"{self.connection_string}/run/{req.workflow_id}/{req.run_id}"
        json_req = self.http_communcatior._proto_to_json(req)
        json_resp = self.http_communcatior.get_request(uri, json_req)
        return self.http_communcatior._json_to_proto(
            json_resp, periodic_pb.GetRunStatusResponse()
        )

    def close(self):
        self.http_communcatior.close()
