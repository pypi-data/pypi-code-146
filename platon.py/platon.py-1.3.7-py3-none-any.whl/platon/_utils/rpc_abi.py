from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Sequence,
    Tuple,
)

from platon_typing import (
    TypeStr,
)
from platon_utils import (
    to_dict,
)
from platon_utils.curried import (
    apply_formatter_at_index,
)
from platon_utils.toolz import (
    curry,
)

from platon._utils.abi import (
    map_abi_data,
)
from platon.types import (
    RPCEndpoint,
)


class RPC:
    # admin
    admin_addPeer = RPCEndpoint("admin_addPeer")
    admin_removePeer = RPCEndpoint("admin_removePeer")
    admin_datadir = RPCEndpoint("admin_datadir")
    admin_nodeInfo = RPCEndpoint("admin_nodeInfo")
    admin_peers = RPCEndpoint("admin_peers")
    admin_startRPC = RPCEndpoint("admin_startRPC")
    admin_startWS = RPCEndpoint("admin_startWS")
    admin_stopRPC = RPCEndpoint("admin_stopRPC")
    admin_stopWS = RPCEndpoint("admin_stopWS")
    admin_importChain = RPCEndpoint("admin_importChain")
    admin_exportChain = RPCEndpoint("admin_exportChain")
    admin_getProgramVersion = RPCEndpoint("admin_getProgramVersion")
    admin_getSchnorrNIZKProve = RPCEndpoint("admin_getSchnorrNIZKProve")
    # admin_setSolc = RPCEndpoint("admin_setSolc")

    # platon
    platon_accounts = RPCEndpoint("platon_accounts")
    platon_blockNumber = RPCEndpoint("platon_blockNumber")
    platon_call = RPCEndpoint("platon_call")
    platon_chainId = RPCEndpoint("platon_chainId")
    platon_estimateGas = RPCEndpoint("platon_estimateGas")
    platon_fillTransaction = RPCEndpoint("platon_fillTransaction")
    platon_gasPrice = RPCEndpoint("platon_gasPrice")
    platon_getAddressHrp = RPCEndpoint("platon_getAddressHrp")
    platon_getBalance = RPCEndpoint("platon_getBalance")
    platon_getBlockByHash = RPCEndpoint("platon_getBlockByHash")
    platon_getBlockByNumber = RPCEndpoint("platon_getBlockByNumber")
    platon_getBlockTransactionCountByHash = RPCEndpoint("platon_getBlockTransactionCountByHash")
    platon_getBlockTransactionCountByNumber = RPCEndpoint("platon_getBlockTransactionCountByNumber")
    platon_getCode = RPCEndpoint("platon_getCode")
    platon_subscribe = RPCEndpoint("platon_subscribe")
    platon_getFilterChanges = RPCEndpoint("platon_getFilterChanges")
    platon_getFilterLogs = RPCEndpoint("platon_getFilterLogs")
    platon_getLogs = RPCEndpoint("platon_getLogs")
    platon_getProof = RPCEndpoint("platon_getProof")
    platon_getStorageAt = RPCEndpoint("platon_getStorageAt")
    platon_getTransactionByBlockHashAndIndex = RPCEndpoint("platon_getTransactionByBlockHashAndIndex")
    platon_getTransactionByBlockNumberAndIndex = RPCEndpoint("platon_getTransactionByBlockNumberAndIndex")
    platon_getTransactionByHash = RPCEndpoint("platon_getTransactionByHash")
    platon_getTransactionCount = RPCEndpoint("platon_getTransactionCount")
    platon_getTransactionReceipt = RPCEndpoint("platon_getTransactionReceipt")
    platon_getWork = RPCEndpoint("platon_getWork")
    platon_mining = RPCEndpoint("platon_mining")
    platon_newBlockFilter = RPCEndpoint("platon_newBlockFilter")
    platon_newFilter = RPCEndpoint("platon_newFilter")
    platon_newPendingTransactionFilter = RPCEndpoint("platon_newPendingTransactionFilter")
    platon_protocolVersion = RPCEndpoint("platon_protocolVersion")
    platon_sendRawTransaction = RPCEndpoint("platon_sendRawTransaction")
    platon_sendTransaction = RPCEndpoint("platon_sendTransaction")
    platon_sign = RPCEndpoint("platon_sign")
    platon_signTransaction = RPCEndpoint("platon_signTransaction")
    platon_signTypedData = RPCEndpoint("platon_signTypedData")
    platon_submitWork = RPCEndpoint("platon_submitWork")
    platon_syncing = RPCEndpoint("platon_syncing")
    platon_uninstallFilter = RPCEndpoint("platon_uninstallFilter")
    platon_evidences = RPCEndpoint("platon_evidences")
    platon_consensusStatus = RPCEndpoint("platon_consensusStatus")
    platon_getPrepareQC = RPCEndpoint("platon_getPrepareQC")

    # evm
    # evm_mine = RPCEndpoint("evm_mine")
    # evm_reset = RPCEndpoint("evm_reset")
    # evm_revert = RPCEndpoint("evm_revert")
    # evm_snapshot = RPCEndpoint("evm_snapshot")

    # miner
    # miner_setExtra = RPCEndpoint("miner_setExtra")
    miner_setGasPrice = RPCEndpoint("miner_setGasPrice")

    # net
    net_listening = RPCEndpoint("net_listening")
    net_peerCount = RPCEndpoint("net_peerCount")
    net_version = RPCEndpoint("net_version")

    # parity
    # parity_addReservedPeer = RPCEndpoint("parity_addReservedPeer")
    # parity_enode = RPCEndpoint("parity_enode")
    # parity_listStorageKeys = RPCEndpoint("parity_listStorageKeys")
    # parity_netPeers = RPCEndpoint("parity_netPeers")
    # parity_mode = RPCEndpoint("parity_mode")
    # parity_setMode = RPCEndpoint("parity_setMode")

    # personal
    personal_ecRecover = RPCEndpoint("personal_ecRecover")
    personal_importRawKey = RPCEndpoint("personal_importRawKey")
    personal_listAccounts = RPCEndpoint("personal_listAccounts")
    personal_listWallets = RPCEndpoint("personal_listWallets")
    personal_lockAccount = RPCEndpoint("personal_lockAccount")
    personal_newAccount = RPCEndpoint("personal_newAccount")
    personal_sendTransaction = RPCEndpoint("personal_sendTransaction")
    personal_sign = RPCEndpoint("personal_sign")
    # personal_signTypedData = RPCEndpoint("personal_signTypedData")
    personal_unlockAccount = RPCEndpoint("personal_unlockAccount")

    # testing
    # testing_timeTravel = RPCEndpoint("testing_timeTravel")

    # debug
    debug_economicConfig = RPCEndpoint("debug_economicConfig")
    debug_getWaitSlashingNodeList = RPCEndpoint("debug_getWaitSlashingNodeList")
    debug_getBadBlocks = RPCEndpoint("debug_getBadBlocks")
    debug_accountRange = RPCEndpoint("debug_accountRange")
    debug_chaindbProperty = RPCEndpoint("debug_chaindbProperty")

    # trace
    # trace_block = RPCEndpoint("trace_block")
    # trace_call = RPCEndpoint("trace_call")
    # trace_filter = RPCEndpoint("trace_filter")
    # trace_rawTransaction = RPCEndpoint("trace_rawTransaction")
    # trace_replayBlockTransactions = RPCEndpoint("trace_replayBlockTransactions")
    # trace_replayTransaction = RPCEndpoint("trace_replayTransaction")
    # trace_transaction = RPCEndpoint("trace_transaction")

    # txpool
    txpool_content = RPCEndpoint("txpool_content")
    txpool_inspect = RPCEndpoint("txpool_inspect")
    txpool_status = RPCEndpoint("txpool_status")

    # web3
    web3_clientVersion = RPCEndpoint("web3_clientVersion")


TRANSACTION_PARAMS_ABIS = {
    'data': 'bytes',
    'from': 'address',
    'gas': 'uint',
    'gasPrice': 'uint',
    'nonce': 'uint',
    'to': 'address',
    'value': 'uint',
}

FILTER_PARAMS_ABIS = {
    'to': 'address',
    'address': 'address[]',
}

TRACE_PARAMS_ABIS = {
    'to': 'address',
    'from': 'address',
}

RPC_ABIS = {
    # platon
    'platon_call': TRANSACTION_PARAMS_ABIS,
    'platon_estimateGas': TRANSACTION_PARAMS_ABIS,
    'platon_getBalance': ['address', None],
    'platon_getBlockByHash': ['bytes32', 'bool'],
    'platon_getBlockTransactionCountByHash': ['bytes32'],
    'platon_getCode': ['address', None],
    'platon_getLogs': FILTER_PARAMS_ABIS,
    'platon_getStorageAt': ['address', 'uint', None],
    'platon_getProof': ['address', 'uint[]', None],
    'platon_getTransactionByBlockHashAndIndex': ['bytes32', 'uint'],
    'platon_getTransactionByHash': ['bytes32'],
    'platon_getTransactionCount': ['address', None],
    'platon_getTransactionReceipt': ['bytes32'],
    'platon_newFilter': FILTER_PARAMS_ABIS,
    'platon_sendRawTransaction': ['bytes'],
    'platon_sendTransaction': TRANSACTION_PARAMS_ABIS,
    'platon_signTransaction': TRANSACTION_PARAMS_ABIS,
    'platon_sign': ['address', 'bytes'],
    'platon_signTypedData': ['address', None],
    'platon_submitWork': ['bytes8', 'bytes32', 'bytes32'],
    # personal
    'personal_sendTransaction': TRANSACTION_PARAMS_ABIS,
    'personal_lockAccount': ['address'],
    'personal_unlockAccount': ['address', None, None],
    'personal_sign': [None, 'address', None],
    'personal_signTypedData': [None, 'address', None],
    'trace_call': TRACE_PARAMS_ABIS,
    # parity
    'parity_listStorageKeys': ['address', None, None, None],
}


@curry
def apply_abi_formatters_to_dict(
        normalizers: Sequence[Callable[[TypeStr, Any], Tuple[TypeStr, Any]]],
        abi_dict: Dict[str, Any],
        data: Dict[Any, Any]
) -> Dict[Any, Any]:
    fields = list(set(abi_dict.keys()) & set(data.keys()))
    formatted_values = map_abi_data(
        normalizers,
        [abi_dict[field] for field in fields],
        [data[field] for field in fields],
    )
    formatted_dict = dict(zip(fields, formatted_values))
    return dict(data, **formatted_dict)


@to_dict
def abi_request_formatters(
        normalizers: Sequence[Callable[[TypeStr, Any], Tuple[TypeStr, Any]]],
        abis: Dict[RPCEndpoint, Any],
) -> Iterable[Tuple[RPCEndpoint, Callable[..., Any]]]:
    for method, abi_types in abis.items():
        if isinstance(abi_types, list):
            yield method, map_abi_data(normalizers, abi_types)
        elif isinstance(abi_types, dict):
            single_dict_formatter = apply_abi_formatters_to_dict(normalizers, abi_types)
            yield method, apply_formatter_at_index(single_dict_formatter, 0)
        else:
            raise TypeError("ABI definitions must be a list or dictionary, got %r" % abi_types)
