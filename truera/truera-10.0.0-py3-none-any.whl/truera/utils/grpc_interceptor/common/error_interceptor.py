from truera.utils.grpc_interceptor import base as grpc_interceptor_base
from truera.utils.truera_status import set_grpc_context_from_truera_error
from truera.utils.truera_status import TruEraError


class TruEraErrorInterceptor(
    grpc_interceptor_base.UnaryServerInterceptor,
    grpc_interceptor_base.StreamServerInterceptor
):
    """An interceptor that catches custom TruEra errors from Python gRPC services. 
    """

    def intercept_unary(self, request, servicer_context, server_info, handler):
        try:
            response = handler(request, servicer_context)
            return response
        except TruEraError as e:
            set_grpc_context_from_truera_error(e, servicer_context)

    def intercept_stream(
        self, request_or_iterator, servicer_context, server_info, handler
    ):
        try:
            response = handler(request_or_iterator, servicer_context)
            return response
        except TruEraError as e:
            set_grpc_context_from_truera_error(e, servicer_context)
