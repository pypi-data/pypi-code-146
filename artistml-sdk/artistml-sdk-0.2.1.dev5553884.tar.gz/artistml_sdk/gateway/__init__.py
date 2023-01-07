from typing import Final

from ._core import Error
from ._core import GrpcClient
from ._core import RPCResponseError
from ._core import try_request_grpc
from ._grpc_clients._kfp import KfpClient
from ._grpc_clients.assoc import AssocClient
from ._grpc_clients.echo import EchoClient
from ._grpc_clients.muses import MusesClient
from ._grpc_clients.tag import TagClient

echo_client: Final[EchoClient] = EchoClient()
muses_client: Final[MusesClient] = MusesClient()
tag_client: Final[TagClient] = TagClient()
assoc_client: Final[AssocClient] = AssocClient()
kfp_client: Final[KfpClient] = KfpClient()
__all__ = [
    "GrpcClient",
    "Error",
    "RPCResponseError",
    "try_request_grpc",
    "echo_client",
    "muses_client",
    "tag_client",
    "assoc_client",
    "kfp_client",
]
