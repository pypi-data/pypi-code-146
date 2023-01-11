"""Implementation of gRPC Python interceptors."""

import collections

import grpc

from truera.utils.grpc_interceptor import base as grpc_interceptor_base


class _UnaryServerInfo(
    collections.namedtuple('_UnaryServerInfo', ('full_method',))
):
    pass


class _StreamServerInfo(
    collections.namedtuple(
        '_StreamServerInfo',
        ('full_method', 'is_client_stream', 'is_server_stream')
    )
):
    pass


class _InterceptorRpcMethodHandler(grpc.RpcMethodHandler):

    def __init__(self, rpc_method_handler, method, interceptor):
        self._rpc_method_handler = rpc_method_handler
        self._method = method
        self._interceptor = interceptor

    @property
    def request_streaming(self):
        return self._rpc_method_handler.request_streaming

    @property
    def response_streaming(self):
        return self._rpc_method_handler.response_streaming

    @property
    def request_deserializer(self):
        return self._rpc_method_handler.request_deserializer

    @property
    def response_serializer(self):
        return self._rpc_method_handler.response_serializer

    @property
    def unary_unary(self):
        if not isinstance(
            self._interceptor, grpc_interceptor_base.UnaryServerInterceptor
        ):
            return self._rpc_method_handler.unary_unary

        def adaptation(request, servicer_context):

            def handler(request, servicer_context):
                return self._rpc_method_handler.unary_unary(
                    request, servicer_context
                )

            return self._interceptor.intercept_unary(
                request, servicer_context, _UnaryServerInfo(self._method),
                handler
            )

        return adaptation

    @property
    def unary_stream(self):
        if not isinstance(
            self._interceptor, grpc_interceptor_base.StreamServerInterceptor
        ):
            return self._rpc_method_handler.unary_stream

        def adaptation(request, servicer_context):

            def handler(request, servicer_context):
                return self._rpc_method_handler.unary_stream(
                    request, servicer_context
                )

            return self._interceptor.intercept_stream(
                request, servicer_context,
                _StreamServerInfo(self._method, False, True), handler
            )

        return adaptation

    @property
    def stream_unary(self):
        if not isinstance(
            self._interceptor, grpc_interceptor_base.StreamServerInterceptor
        ):
            return self._rpc_method_handler.stream_unary

        def adaptation(request_iterator, servicer_context):

            def handler(request_iterator, servicer_context):
                return self._rpc_method_handler.stream_unary(
                    request_iterator, servicer_context
                )

            return self._interceptor.intercept_stream(
                request_iterator, servicer_context,
                _StreamServerInfo(self._method, True, False), handler
            )

        return adaptation

    @property
    def stream_stream(self):
        if not isinstance(
            self._interceptor, grpc_interceptor_base.StreamServerInterceptor
        ):
            return self._rpc_method_handler.stream_stream

        def adaptation(request_iterator, servicer_context):

            def handler(request_iterator, servicer_context):
                return self._rpc_method_handler.stream_stream(
                    request_iterator, servicer_context
                )

            return self._interceptor.intercept_stream(
                request_iterator, servicer_context,
                _StreamServerInfo(self._method, True, True), handler
            )

        return adaptation


class _InterceptorGenericRpcHandler(grpc.GenericRpcHandler):

    def __init__(self, generic_rpc_handler, interceptor):
        self.generic_rpc_handler = generic_rpc_handler
        self._interceptor = interceptor

    def service(self, handler_call_details):
        result = self.generic_rpc_handler.service(handler_call_details)
        if result:
            result = _InterceptorRpcMethodHandler(
                result, handler_call_details.method, self._interceptor
            )
        return result


class _InterceptorServer(grpc.Server):

    def __init__(self, server, interceptor):
        self._server = server
        self._interceptor = interceptor

    def add_generic_rpc_handlers(self, generic_rpc_handlers):
        generic_rpc_handlers = [
            _InterceptorGenericRpcHandler(
                generic_rpc_handler, self._interceptor
            ) for generic_rpc_handler in generic_rpc_handlers
        ]
        return self._server.add_generic_rpc_handlers(generic_rpc_handlers)

    def add_insecure_port(self, *args, **kwargs):
        return self._server.add_insecure_port(*args, **kwargs)

    def add_secure_port(self, *args, **kwargs):
        return self._server.add_secure_port(*args, **kwargs)

    def start(self, *args, **kwargs):
        return self._server.start(*args, **kwargs)

    def stop(self, *args, **kwargs):
        return self._server.stop(*args, **kwargs)


def intercept_server(server, *interceptors):
    if isinstance(server, _InterceptorServer):
        raise IllegalStateError(
            'server already has interceptors. Please add all interceptors in the same call.'
        )

    result = server
    for interceptor in interceptors:
        # TODO(apoorv) Why is this necessary.
        if not isinstance(interceptor, grpc_interceptor_base.UnaryServerInterceptor) and \
           not isinstance(interceptor, grpc_interceptor_base.StreamServerInterceptor):
            raise TypeError(
                'interceptor must be either a '
                'grpc_interceptor_base.UnaryServerInterceptor or a '
                'grpc_interceptor_base.StreamServerInterceptor'
            )
        result = _InterceptorServer(result, interceptor)
    return result


class IllegalStateError(ValueError):
    """Raised when a server is in an incorrect state."""
