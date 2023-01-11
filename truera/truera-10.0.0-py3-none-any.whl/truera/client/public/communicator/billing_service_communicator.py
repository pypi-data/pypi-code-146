from abc import ABC
from abc import abstractmethod

from truera.protobuf.billing import billing_service_pb2 as billing_pb


class BillingServiceCommunicator(ABC):

    @abstractmethod
    def list_billing_metrics(
        self,
        req: billing_pb.ListBillingMetricsRequest,
        request_context=None
    ) -> billing_pb.ListBillingMetricsResponse:
        pass

    @abstractmethod
    def generate_report(
        self,
        req: billing_pb.GenerateUsageReportRequest,
        request_context=None
    ) -> billing_pb.GenerateUsageReportResponse:
        pass

    @abstractmethod
    def list_audit_summary_metrics(
        self,
        req: billing_pb.ListAuditSummaryMetricsRequest,
        request_context=None
    ) -> billing_pb.ListAuditSummaryMetricsResponse:
        pass

    @abstractmethod
    def generate_audit_summary_report(
        self,
        req: billing_pb.GenerateAuditSummaryReportRequest,
        request_context=None
    ) -> billing_pb.GenerateAuditSummaryReportResponse:
        pass
