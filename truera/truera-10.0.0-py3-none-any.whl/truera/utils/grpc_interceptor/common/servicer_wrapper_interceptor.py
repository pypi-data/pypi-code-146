from google.protobuf import any_pb2
from google.rpc.status_pb2 import Status
from grpc import ServicerContext
from grpc import StatusCode
from grpc_status.rpc_status import to_status

from truera.protobuf.public.error_details_pb2 import \
    ErrorDetails  # pylint: disable=no-name-in-module
from truera.utils.grpc_interceptor import base as grpc_interceptor_base


# A ServicerContext that wraps another ServicerContext, with special handling for abort and
# abort_with_status methods.
# Useful for logging of RPCs that were explicitly aborted (instead of failed due to unexpected
# exceptions.)
class ServicerContextWrapper(ServicerContext):

    def __init__(self, wrapped, friendly_name) -> None:
        self.__wrapped = wrapped
        self.__is_aborted = False
        self.__audit_event = dict()
        self.__friendly_name = friendly_name
        self.__user_id = None
        self.__user_name = None

    def abort(self, code: StatusCode, message: str):
        return self.abort_with_details(code, message, ErrorDetails())

    def abort_with_status(self, status: Status):
        return self.__wrapped.abort_with_status(status)

    # pylint: disable=no-member
    def abort_with_details(
        self, code: StatusCode, message: str, details: ErrorDetails
    ):
        self.__is_aborted = True
        self._add_error_details_if_not_set(details)
        packed_details = any_pb2.Any()
        packed_details.Pack(details)
        google_status_obj = Status(
            code=code.value[0], message=message, details=[packed_details]
        )
        return self.__wrapped.abort_with_status(to_status(google_status_obj))

    def _add_error_details_if_not_set(self, details: ErrorDetails):
        if not details.source_service:
            details.source_service = self.friendly_name

    @property
    def is_aborted(self):
        """Set if the RPC is explicitly aborted by the server.
        NOTE: This will not be true if an unhandled exception causes
        RPC failure.
        """
        return self.__is_aborted

    @property
    def code(self):
        return self.__wrapped.code

    @property
    def details(self):
        return self.__wrapped.details()

    @property
    def audit_event(self):
        return self.__audit_event

    @property
    def friendly_name(self):
        return self.__friendly_name

    @property
    def user_id(self):
        return self.__user_id

    @property
    def user_name(self):
        return self.__user_name

    def invocation_metadata(self):
        return self.__wrapped.invocation_metadata()

    def peer(self):
        return self.__wrapped.peer()

    def peer_identities(self):
        return self.__wrapped.peer_identities()

    def peer_identity_key(self):
        return self.__wrapped.peer_identity_key()

    def auth_context(self):
        return self.__wrapped.auth_context()

    def set_compression(self, compression):
        return self.__wrapped.set_compression(compression)

    def send_initial_metadata(self, initial_metadata):
        return self.__wrapped.send_initial_metadata(initial_metadata)

    def set_trailing_metadata(self, trailing_metadata):
        return self.__wrapped.set_trailing_metadata(trailing_metadata)

    def set_code(self, code):
        return self.__wrapped.set_code(code)

    def set_details(self, details):
        return self.__wrapped.set_details(details)

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_user_name(self, user_name):
        self.__user_name = user_name

    def disable_next_message_compression(self):
        return self.__wrapped.disable_next_message_compression()

    def is_active(self):
        return self.__wrapped.is_active()

    def time_remaining(self):
        return self.__wrapped.time_remaining()

    def cancel(self):
        return self.__wrapped.cancel()

    def add_callback(self, callback):
        return self.__wrapped.add_callback(callback)


class ServicerWrapperInterceptor(
    grpc_interceptor_base.UnaryServerInterceptor,
    grpc_interceptor_base.StreamServerInterceptor
):

    def intercept_unary(self, request, servicer_context, server_info, handler):
        friendly_name = server_info.full_method[1:].replace("/", ".")
        servicer_context_wrapper = ServicerContextWrapper(
            servicer_context, friendly_name
        )
        return handler(request, servicer_context_wrapper)

    def intercept_stream(
        self, request_or_iterator, servicer_context, server_info, handler
    ):
        friendly_name = server_info.full_method[1:].replace("/", ".")
        servicer_context_wrapper = ServicerContextWrapper(
            servicer_context, friendly_name
        )
        response = handler(request_or_iterator, servicer_context_wrapper)
        return response
