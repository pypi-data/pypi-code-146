import threading

import grpc

from truera.authn import usercontext
from truera.utils.grpc_interceptor import base as grpc_interceptor_base


class AuthContext(threading.local):

    def __init__(self):
        self._request_context = None
        self._grpc_context = None

    def _set_auth_context(
        self,
        *,
        request_context: usercontext.RequestContext = None,
        grpc_context: grpc.ServicerContext = None
    ):
        assert self._request_context is None, 'Consistency error: user_context is not None'
        assert self._grpc_context is None, 'Consistency error: grpc_context is not None'

        self._request_context = request_context
        self._grpc_context = grpc_context

    @property
    def user_context(self) -> usercontext.UserContext:
        return self._request_context.get_user_context()

    @property
    def request_context(self) -> usercontext.RequestContext:
        return self._request_context

    @property
    def grpc_context(self) -> grpc.ServicerContext:
        return self._grpc_context

    def clear_context(self):
        self._request_context = None
        self._grpc_context = None


auth_context = AuthContext()


class AuthServerInterceptor(
    grpc_interceptor_base.UnaryServerInterceptor,
    grpc_interceptor_base.StreamServerInterceptor
):

    def __init__(
        self, request_context_helper: usercontext.RequestContextHelper
    ):
        self._request_context_helper = request_context_helper

    def intercept_stream(
        self, request_or_iterator, servicer_context, server_info, handler
    ):
        try:
            request_context = self._request_context_helper.create_request_context_grpc(
                servicer_context
            )
            user_context = request_context.get_user_context()
            servicer_context.set_user_id(user_context.get_id())
            servicer_context.set_user_name(user_context.get_name())
            auth_context._set_auth_context(
                request_context=request_context, grpc_context=servicer_context
            )

            return handler(request_or_iterator, servicer_context)

        finally:
            auth_context.clear_context()

    def intercept_unary(self, request, servicer_context, server_info, handler):
        try:
            request_context = self._request_context_helper.create_request_context_grpc(
                servicer_context
            )
            user_context = request_context.get_user_context()
            servicer_context.set_user_id(user_context.get_id())
            servicer_context.set_user_name(user_context.get_name())
            auth_context._set_auth_context(
                request_context=request_context, grpc_context=servicer_context
            )

            return handler(request, servicer_context)

        finally:
            auth_context.clear_context()
