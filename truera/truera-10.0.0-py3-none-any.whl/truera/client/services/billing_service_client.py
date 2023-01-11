import datetime
import logging
from typing import List, Union

from google.protobuf.timestamp_pb2 import \
    Timestamp  # pylint: disable=no-name-in-module

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.billing_service_communicator import \
    BillingServiceCommunicator
from truera.client.public.communicator.billing_service_http_communicator import \
    HttpBillingServiceCommunicator
from truera.protobuf.billing import billing_service_pb2 as billing_pb
from truera.protobuf.public.util import time_range_pb2 as tr_pb


class BillingServiceClient:

    def __init__(
        self, communicator: BillingServiceCommunicator, logger=None
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
            communicator = HttpBillingServiceCommunicator(
                connection_string,
                auth_details,
                logger,
                verify_cert=verify_cert
            )
        else:
            from truera.client.private.communicator.billing_service_grpc_communicator import \
                GrpcBillingServiceCommunicator
            communicator = GrpcBillingServiceCommunicator(
                connection_string, auth_details, logger
            )
        return BillingServiceClient(communicator, logger)

    def list_billing_metrics(self, request_context=None):
        req = billing_pb.ListBillingMetricsRequest()
        billing_metrics = self.communicator.list_billing_metrics(
            req, request_context=request_context
        ).metrics
        return [billing_pb.BillingMetrics.Name(m) for m in billing_metrics]

    def generate_report(
        self, start_date_str, end_date_str, request_context=None
    ):
        # start date and end date are assumed to be in UTC timezone.
        date_format = "%m-%d-%Y"
        try:
            start_datetime = datetime.datetime.strptime(
                start_date_str, date_format
            )
            end_datetime = datetime.datetime.strptime(end_date_str, date_format)
        except ValueError:
            raise ValueError(
                "Incorrect date format, Please use {}".format(date_format)
            )

        start_time = Timestamp()
        start_time.FromDatetime(start_datetime)

        end_time = Timestamp()
        end_time.FromDatetime(end_datetime)

        time_range = tr_pb.TimeRange(begin=start_time, end=end_time)
        req = billing_pb.GenerateUsageReportRequest(reportDateRange=time_range)
        return self.communicator.generate_report(
            req, request_context=request_context
        )

    def list_audit_summary_metrics(self, request_context=None):
        req = billing_pb.ListAuditSummaryMetricsRequest()
        audit_summary_metrics = self.communicator.list_audit_summary_metrics(
            req, request_context=request_context
        ).metrics
        return [
            billing_pb.AuditSummaryMetrics.Name(m)
            for m in audit_summary_metrics
        ]

    def generate_audit_summary_report(
        self,
        metrics: List[str],
        start_datetime_str: str,
        end_datetime_str: str,
        request_context=None
    ):
        req = self._create_audit_summary_report_request(
            metrics=metrics,
            start_datetime_str=start_datetime_str,
            end_datetime_str=end_datetime_str
        )
        return self.communicator.generate_audit_summary_report(
            req, request_context=request_context
        )

    def _create_audit_summary_report_request(
        self, metrics: List[str], start_datetime_str: str, end_datetime_str: str
    ) -> billing_pb.GenerateAuditSummaryReportRequest:
        # start date and end date are assumed to be in UTC timezone.
        date_format = "%m-%d-%Y %H:%M%z"
        utc_tz_suffix = "+0000"
        try:
            start_datetime = datetime.datetime.strptime(
                start_datetime_str + utc_tz_suffix, date_format
            )
            end_datetime = datetime.datetime.strptime(
                end_datetime_str + utc_tz_suffix, date_format
            )
        except ValueError:
            raise ValueError(
                "Incorrect date format, Please use {}".format(date_format)
            )

        start_time = Timestamp()
        start_time.FromDatetime(start_datetime)

        end_time = Timestamp()
        end_time.FromDatetime(end_datetime)

        audit_metrics = [
            billing_pb.AuditSummaryMetrics.Value(m) for m in metrics
        ]
        time_range = tr_pb.TimeRange(begin=start_time, end=end_time)
        return billing_pb.GenerateAuditSummaryReportRequest(
            reportDateRange=time_range, metrics=audit_metrics
        )
