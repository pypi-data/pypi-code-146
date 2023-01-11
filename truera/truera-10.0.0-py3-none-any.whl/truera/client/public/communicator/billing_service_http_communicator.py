import logging
from typing import Union

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.billing_service_communicator import \
    BillingServiceCommunicator
from truera.client.public.communicator.http_communicator import \
    HttpCommunicator
from truera.protobuf.billing import billing_service_pb2 as billing_pb


class HttpBillingServiceCommunicator(BillingServiceCommunicator):

    def __init__(
        self,
        connection_string: str,
        auth_details: AuthDetails,
        logger: logging.Logger,
        *,
        verify_cert: Union[bool, str] = True
    ):
        connection_string = connection_string.rstrip("/")
        self.connection_string = f"{connection_string}/api/billingservice/billing"
        self.http_communicator = HttpCommunicator(
            connection_string=self.connection_string,
            auth_details=auth_details,
            logger=logger,
            verify_cert=verify_cert
        )

    def list_billing_metrics(
        self,
        req: billing_pb.ListBillingMetricsRequest,
        request_context=None
    ) -> billing_pb.ListBillingMetricsResponse:
        uri = "{conn}/metrics".format(conn=self.connection_string)
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, billing_pb.ListBillingMetricsResponse()
        )

    def generate_report(
        self,
        req: billing_pb.GenerateUsageReportRequest,
        request_context=None
    ) -> billing_pb.GenerateUsageReportResponse:
        uri = "{conn}/report/generate".format(conn=self.connection_string)
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, billing_pb.GenerateUsageReportResponse()
        )

    def list_audit_summary_metrics(
        self,
        req: billing_pb.ListAuditSummaryMetricsRequest,
        request_context=None
    ) -> billing_pb.ListAuditSummaryMetricsResponse:
        uri = "{conn}/audit-summary-metrics".format(conn=self.connection_string)
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, billing_pb.ListAuditSummaryMetricsResponse()
        )

    def generate_audit_summary_report(
        self,
        req: billing_pb.GenerateAuditSummaryReportRequest,
        request_context=None
    ) -> billing_pb.GenerateAuditSummaryReportResponse:
        uri = "{conn}/audit-summary-report/generate".format(
            conn=self.connection_string
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, billing_pb.GenerateAuditSummaryReportResponse()
        )
