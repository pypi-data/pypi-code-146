from typing import Optional

from chalk.client.client_impl import ChalkAPIClientImpl
from chalk.client.client_protocol import (
    ChalkAPIClientProtocol,
    ChalkBaseException,
    ChalkError,
    ChalkException,
    ErrorCode,
    ErrorCodeCategory,
    FeatureResult,
    OfflineQueryContext,
    OnlineQueryContext,
    OnlineQueryResponse,
    WhoAmIResponse,
)

__all__ = [
    "ChalkError",
    "FeatureResult",
    "WhoAmIResponse",
    "OnlineQueryResponse",
    "ChalkBaseException",
    "ChalkAPIClientProtocol",
    "OnlineQueryContext",
    "OfflineQueryContext",
    "ErrorCode",
    "ErrorCodeCategory",
    "ChalkException",
    "ChalkClient",
]


def ChalkClient(
    *,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    environment: Optional[str] = None,
    api_server: Optional[str] = None,
) -> ChalkAPIClientProtocol:
    return ChalkAPIClientImpl(
        client_id=client_id,
        client_secret=client_secret,
        environment=environment,
        api_server=api_server,
    )
