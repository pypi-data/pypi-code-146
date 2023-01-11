import datetime
import os

from truera.utils.audit_logger import AuditLogger
from truera.utils.config_util import get_config_value
from truera.utils.grpc_interceptor import base as grpc_interceptor_base
from truera.utils.grpc_interceptor.common.servicer_wrapper_interceptor import \
    ServicerContextWrapper


class AuditInterceptor(
    grpc_interceptor_base.UnaryServerInterceptor,
    grpc_interceptor_base.StreamServerInterceptor
):

    def __init__(
        self, service_name, metric_labels, audit_log_dir, emit_to_prometheus
    ):
        log_file = os.path.join(audit_log_dir, f"audit_{service_name}.log")
        self.audit_logger = AuditLogger(
            service_name,
            log_file=log_file,
            emit_to_prometheus=emit_to_prometheus,
            labels=metric_labels
        )
        self.audit_log_dir = audit_log_dir

    def intercept_stream(
        self, request_or_iterator, servicer_context, server_info, handler
    ):
        start_time = datetime.datetime.now().isoformat()
        try:
            return handler(request_or_iterator, servicer_context)
        except Exception as e:
            servicer_context.audit_event["error_message"] = str(e)
            raise e
        finally:
            servicer_context.audit_event["user_id"] = servicer_context.user_id
            servicer_context.audit_event["user_name"
                                        ] = servicer_context.user_name
            servicer_context.audit_event["api_name"
                                        ] = servicer_context.friendly_name
            servicer_context.audit_event["code"] = str(servicer_context.code)
            servicer_context.audit_event["start_time"] = start_time
            servicer_context.audit_event["end_time"] = datetime.datetime.now(
            ).isoformat()

            if servicer_context.is_aborted:
                servicer_context.audit_event["error_message"
                                            ] = servicer_context.details
            self.audit_logger.log(servicer_context.audit_event)

    def intercept_unary(
        self, request, servicer_context: ServicerContextWrapper, server_info,
        handler
    ):
        start_time = datetime.datetime.now().isoformat()
        try:
            return handler(request, servicer_context)
        except Exception as e:
            servicer_context.audit_event["error_message"] = str(e)
            raise e
        finally:
            servicer_context.audit_event["user_id"] = servicer_context.user_id
            servicer_context.audit_event["user_name"
                                        ] = servicer_context.user_name
            servicer_context.audit_event["api_name"
                                        ] = servicer_context.friendly_name
            servicer_context.audit_event["code"] = str(servicer_context.code)
            servicer_context.audit_event["start_time"] = start_time
            servicer_context.audit_event["end_time"] = datetime.datetime.now(
            ).isoformat()

            if servicer_context.is_aborted:
                servicer_context.audit_event["error_message"
                                            ] = servicer_context.details
            self.audit_logger.log(servicer_context.audit_event)
