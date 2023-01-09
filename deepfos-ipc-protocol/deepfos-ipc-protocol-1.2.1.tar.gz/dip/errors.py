

class DeepFOSError(Exception):
    """Base exception for this package"""


class ProtocolError(DeepFOSError):
    """Base exception related to protocol"""


class DeepFOSIOError(DeepFOSError):
    """Base exception related to I/O"""


class DuplicateProtoError(ProtocolError):
    """Duplicated message type found in registered protocl"""


class UnsupportedProtoError(ProtocolError):
    """Unknown protocol"""


class ProtoEncodeError(ProtocolError):
    """Message"""


class ProtoDecodeError(ProtocolError):
    pass


class ReadTimeout(DeepFOSIOError):
    pass


class ConnectionError(DeepFOSIOError):
    pass


class ConnectionClosed(DeepFOSIOError):
    pass


class ConnectionAquireTimeout(DeepFOSIOError):
    pass


class ResponseError(DeepFOSIOError):
    pass
