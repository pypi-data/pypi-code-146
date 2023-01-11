from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Collection,
    Type,
)

from requests.exceptions import (
    ConnectionError,
    HTTPError,
    Timeout,
    TooManyRedirects,
)

from platon.types import (
    RPCEndpoint,
    RPCResponse,
)

if TYPE_CHECKING:
    from platon import Web3

whitelist = [
    'admin',
    'miner',
    'net',
    'txpool'
    'testing',
    'evm',
    'platon_protocolVersion',
    'platon_syncing',
    'platon_coinbase',
    'platon_mining',
    'platon_gasPrice',
    'platon_accounts',
    'platon_blockNumber',
    'platon_getBalance',
    'platon_getStorageAt',
    'platon_getProof',
    'platon_getCode',
    'platon_getBlockByNumber',
    'platon_getBlockByHash',
    'platon_getBlockTransactionCountByNumber',
    'platon_getBlockTransactionCountByHash',
    'platon_getTransactionByHash',
    'platon_getTransactionByBlockHashAndIndex',
    'platon_getTransactionByBlockNumberAndIndex',
    'platon_getTransactionReceipt',
    'platon_getTransactionCount',
    'platon_call',
    'platon_estimateGas',
    'platon_newBlockFilter',
    'platon_newPendingTransactionFilter',
    'platon_newFilter',
    'platon_getFilterChanges',
    'platon_getFilterLogs',
    'platon_getLogs',
    'platon_uninstallFilter',
    'platon_getCompilers',
    'platon_getWork',
    'platon_sign',
    'platon_signTypedData',
    'platon_sendRawTransaction',
    'personal_importRawKey',
    'personal_newAccount',
    'personal_listAccounts',
    'personal_listWallets',
    'personal_lockAccount',
    'personal_unlockAccount',
    'personal_ecRecover',
    'personal_sign',
    'personal_signTypedData',
]


def check_if_retry_on_failure(method: RPCEndpoint) -> bool:
    root = method.split('_')[0]
    if root in whitelist:
        return True
    elif method in whitelist:
        return True
    else:
        return False


def exception_retry_middleware(
    make_request: Callable[[RPCEndpoint, Any], RPCResponse],
    web3: "Web3",
    errors: Collection[Type[BaseException]],
    retries: int = 5,
) -> Callable[[RPCEndpoint, Any], RPCResponse]:
    """
    Creates middleware that retries failed HTTP requests. Is a default
    middleware for HTTPProvider.
    """
    def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
        if check_if_retry_on_failure(method):
            for i in range(retries):
                try:
                    return make_request(method, params)
                # https://github.com/python/mypy/issues/5349
                except errors:  # type: ignore
                    if i < retries - 1:
                        continue
                    else:
                        raise
            return None
        else:
            return make_request(method, params)
    return middleware


def http_retry_request_middleware(
    make_request: Callable[[RPCEndpoint, Any], Any], web3: "Web3"
) -> Callable[[RPCEndpoint, Any], Any]:
    return exception_retry_middleware(
        make_request,
        web3,
        (ConnectionError, HTTPError, Timeout, TooManyRedirects)
    )
