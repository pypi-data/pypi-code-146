import traceback
from functools import wraps

import grpc

from ...logger import get_logger

LOGGER = get_logger()


def try_request_grpc(func):
    """try to request gRPC service decorator"""

    @wraps(func)
    def helper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (grpc.RpcError, TimeoutError) as err:
            LOGGER.exception(err)
            raise err
        except:
            LOGGER.fatal(f"unexpected client error: {traceback.format_exc()}")
            raise

    return helper


class Error(Exception):
    """Common error type of client."""


class RPCResponseError(Error):
    """Represents an error from RPC call response."""

    def __init__(self, response):
        super().__init__(response)
        self.code = response.code
        self.message = response.message
