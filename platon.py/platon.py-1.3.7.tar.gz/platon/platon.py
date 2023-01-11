from typing import (
    Any,
    Callable,
    List,
    NoReturn,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
    overload,
)
import warnings

from platon_account import (
    Account,
)
from platon_typing import (
    Address,
    BlockNumber,
    Bech32Address,
    HexStr,
)
from platon_utils import (
    is_bech32_address,
    is_string,
)
from platon_utils.toolz import (
    assoc,
    merge,
)
from hexbytes import (
    HexBytes,
)

from platon._utils.blocks import (
    select_method_for_block_identifier,
)
from platon._utils.empty import (
    Empty,
    empty,
)
from platon._utils.encoding import (
    to_hex,
)
from platon._utils.filters import (
    select_filter_method,
)
from platon._utils.rpc_abi import (
    RPC,
)
from platon._utils.threads import (
    Timeout,
)
from platon._utils.transactions import (
    assert_valid_transaction_params,
    extract_valid_transaction_params,
    get_required_transaction,
    replace_transaction,
    wait_for_transaction_receipt,
)
from platon.contract import (
    ConciseContract,
    Contract,
    ContractCaller,
)
from platon.exceptions import (
    TimeExhausted,
)
from platon.iban import (
    Iban,
)
from platon.method import (
    Method,
    default_root_munger,
)
from platon.module import (
    Module,
)
from platon.types import (
    ENS,
    BlockData,
    BlockIdentifier,
    CallOverrideParams,
    FilterParams,
    GasPriceStrategy,
    LogReceipt,
    MerkleProof,
    Nonce,
    SignedTx,
    SyncStatus,
    TxData,
    TxParams,
    TxReceipt,
    Von,
    _Hash32,
    UnFillTxParams,
)


class BasePlaton(Module):
    _default_account: Union[Bech32Address, Empty] = empty
    gasPriceStrategy = None

    _gas_price: Method[Callable[[], Von]] = Method(
        RPC.platon_gasPrice,
        mungers=None,
    )

    @property
    def default_account(self) -> Union[Bech32Address, Empty]:
        return self._default_account

    def send_transaction_munger(self, transaction: TxParams) -> Tuple[TxParams]:
        if 'from' not in transaction and is_bech32_address(self.default_account):
            transaction = assoc(transaction, 'from', self.default_account)

        return (transaction,)

    _send_transaction: Method[Callable[[TxParams], HexBytes]] = Method(
        RPC.platon_sendTransaction,
        mungers=[send_transaction_munger]
    )

    fill_transaction_munger = send_transaction_munger

    fill_transaction: Method[Callable[[UnFillTxParams], TxParams]] = Method(
        RPC.platon_fillTransaction,
        mungers=[fill_transaction_munger]
    )

    _get_transaction: Method[Callable[[_Hash32], TxData]] = Method(
        RPC.platon_getTransactionByHash,
        mungers=[default_root_munger]
    )

    def _generate_gas_price(self, transaction_params: Optional[TxParams] = None) -> Optional[Von]:
        if self.gasPriceStrategy:
            return self.gasPriceStrategy(self.web3, transaction_params)
        return None

    def set_gas_price_strategy(self, gas_price_strategy: GasPriceStrategy) -> None:
        self.gasPriceStrategy = gas_price_strategy

    def estimate_gas_munger(
            self,
            transaction: TxParams,
            block_identifier: Optional[BlockIdentifier] = None
    ) -> Sequence[Union[TxParams, BlockIdentifier]]:
        if 'from' not in transaction and is_bech32_address(self.default_account):
            transaction = assoc(transaction, 'from', self.default_account)

        if block_identifier is None:
            params: Sequence[Union[TxParams, BlockIdentifier]] = [transaction]
        else:
            params = [transaction, block_identifier]

        return params

    _estimate_gas: Method[Callable[..., Von]] = Method(
        RPC.platon_estimateGas,
        mungers=[estimate_gas_munger]
    )

    def get_block_munger(
            self, block_identifier: BlockIdentifier, full_transactions: bool = False
    ) -> Tuple[BlockIdentifier, bool]:
        return (block_identifier, full_transactions)

    """
    `platon_getBlockByHash`
    `platon_getBlockByNumber`
    """
    _get_block: Method[Callable[..., BlockData]] = Method(
        method_choice_depends_on_args=select_method_for_block_identifier(
            if_predefined=RPC.platon_getBlockByNumber,
            if_hash=RPC.platon_getBlockByHash,
            if_number=RPC.platon_getBlockByNumber,
        ),
        mungers=[get_block_munger],
    )

    get_block_number: Method[Callable[[], BlockNumber]] = Method(
        RPC.platon_blockNumber,
        mungers=None,
    )

    evidences: Method[Callable[[], str]] = Method(
        RPC.platon_evidences,
        mungers=None,
    )

    consensus_status: Method[Callable[[], str]] = Method(
        RPC.platon_consensusStatus,
        mungers=None,
    )

    get_prepare_QC: Method[Callable[[], str]] = Method(
        RPC.platon_getPrepareQC,
        mungers=None,
    )


class AsyncPlaton(BasePlaton):
    is_async = True

    @property
    async def gas_price(self) -> Von:
        # types ignored b/c mypy conflict with BlockingPlaton properties
        return await self._gas_price()  # type: ignore

    async def send_transaction(self, transaction: TxParams) -> HexBytes:
        # types ignored b/c mypy conflict with BlockingPlaton properties
        return await self._send_transaction(transaction)  # type: ignore

    async def get_transaction(self, transaction_hash: _Hash32) -> TxData:
        # types ignored b/c mypy conflict with BlockingPlaton properties
        return await self._get_transaction(transaction_hash)  # type: ignore

    async def generate_gas_price(
            self, transaction_params: Optional[TxParams] = None
    ) -> Optional[Von]:
        return self._generate_gas_price(transaction_params)

    async def estimate_gas(
            self,
            transaction: TxParams,
            block_identifier: Optional[BlockIdentifier] = None
    ) -> Von:
        # types ignored b/c mypy conflict with BlockingPlaton properties
        return await self._estimate_gas(transaction, block_identifier)  # type: ignore

    async def get_block(
            self, block_identifier: BlockIdentifier, full_transactions: bool = False
    ) -> BlockData:
        # types ignored b/c mypy conflict with BlockingPlaton properties
        return await self._get_block(block_identifier, full_transactions)  # type: ignore

    @property
    async def block_number(self) -> BlockNumber:
        # types ignored b/c mypy conflict with BlockingPlaton properties
        return await self.get_block_number()  # type: ignore


class Platon(BasePlaton, Module):
    account = Account()
    _default_block: BlockIdentifier = "latest"
    # todo: add wasm contract
    defaultContractFactory: Type[Union[Contract, ConciseContract, ContractCaller]] = Contract
    iban = Iban

    def namereg(self) -> NoReturn:
        raise NotImplementedError()

    def icapNamereg(self) -> NoReturn:
        raise NotImplementedError()

    _protocol_version: Method[Callable[[], str]] = Method(
        RPC.platon_protocolVersion,
        mungers=None,
    )

    @property
    def protocol_version(self) -> str:
        warnings.warn(
            "This method has been deprecated in some clients.",
            category=DeprecationWarning,
        )
        return self._protocol_version()

    is_syncing: Method[Callable[[], Union[SyncStatus, bool]]] = Method(
        RPC.platon_syncing,
        mungers=None,
    )

    @property
    def syncing(self) -> Union[SyncStatus, bool]:
        return self.is_syncing()

    @property
    def gas_price(self) -> Von:
        return self._gas_price()

    get_accounts: Method[Callable[[], Tuple[Bech32Address]]] = Method(
        RPC.platon_accounts,
        mungers=None,
    )

    @property
    def accounts(self) -> Tuple[Bech32Address]:
        return self.get_accounts()

    @property
    def block_number(self) -> BlockNumber:
        return self.get_block_number()

    _chain_id: Method[Callable[[], int]] = Method(
        RPC.platon_chainId,
        mungers=None,
    )

    @property
    def chain_id(self) -> int:
        return self._chain_id()

    """ property default_account """

    @property
    def default_account(self) -> Union[Bech32Address, Empty]:
        return self._default_account

    @default_account.setter
    def default_account(self, account: Union[Bech32Address, Empty]) -> None:
        self._default_account = account

    """ property default_block """

    @property
    def default_block(self) -> BlockIdentifier:
        return self._default_block

    @default_block.setter
    def default_block(self, value: BlockIdentifier) -> None:
        self._default_block = value

    def block_id_munger(
            self,
            account: Union[Address, Bech32Address, ENS],
            block_identifier: Optional[BlockIdentifier] = None
    ) -> Tuple[Union[Address, Bech32Address, ENS], BlockIdentifier]:
        if block_identifier is None:
            block_identifier = self.default_block
        return (account, block_identifier)

    get_balance: Method[Callable[..., Von]] = Method(
        RPC.platon_getBalance,
        mungers=[block_id_munger],
    )

    def get_storage_at_munger(
            self,
            account: Union[Address, Bech32Address, ENS],
            position: int,
            block_identifier: Optional[BlockIdentifier] = None
    ) -> Tuple[Union[Address, Bech32Address, ENS], int, BlockIdentifier]:
        if block_identifier is None:
            block_identifier = self.default_block
        return (account, position, block_identifier)

    get_storage_at: Method[Callable[..., HexBytes]] = Method(
        RPC.platon_getStorageAt,
        mungers=[get_storage_at_munger],
    )

    def get_proof_munger(
            self,
            account: Union[Address, Bech32Address, ENS],
            positions: Sequence[int],
            block_identifier: Optional[BlockIdentifier] = None
    ) -> Tuple[Union[Address, Bech32Address, ENS], Sequence[int], Optional[BlockIdentifier]]:
        if block_identifier is None:
            block_identifier = self.default_block
        return (account, positions, block_identifier)

    get_proof: Method[
        Callable[
            [Tuple[Union[Address, Bech32Address, ENS], Sequence[int], Optional[BlockIdentifier]]],
            MerkleProof
        ]
    ] = Method(
        RPC.platon_getProof,
        mungers=[get_proof_munger],
    )

    get_code: Method[Callable[..., HexBytes]] = Method(
        RPC.platon_getCode,
        mungers=[block_id_munger]
    )

    _get_address_hrp: Method[Callable[[], str]] = Method(
        RPC.platon_getAddressHrp,
        mungers=None,
    )

    def get_address_hrp(self) -> int:
        return self._get_address_hrp()

    def get_block(
            self, block_identifier: BlockIdentifier, full_transactions: bool = False
    ) -> BlockData:
        return self._get_block(block_identifier, full_transactions)

    """
    `platon_getBlockTransactionCountByHash`
    `platon_getBlockTransactionCountByNumber`
    """
    get_block_transaction_count: Method[Callable[[BlockIdentifier], int]] = Method(
        method_choice_depends_on_args=select_method_for_block_identifier(
            if_predefined=RPC.platon_getBlockTransactionCountByNumber,
            if_hash=RPC.platon_getBlockTransactionCountByHash,
            if_number=RPC.platon_getBlockTransactionCountByNumber,
        ),
        mungers=[default_root_munger]
    )

    def get_transaction(self, transaction_hash: _Hash32) -> TxData:
        return self._get_transaction(transaction_hash)

    get_transaction_by_block: Method[Callable[[BlockIdentifier, int], TxData]] = Method(
        method_choice_depends_on_args=select_method_for_block_identifier(
            if_predefined=RPC.platon_getTransactionByBlockNumberAndIndex,
            if_hash=RPC.platon_getTransactionByBlockHashAndIndex,
            if_number=RPC.platon_getTransactionByBlockNumberAndIndex,
        ),
        mungers=[default_root_munger]
    )

    def wait_for_transaction_receipt(
            self, transaction_hash: _Hash32, timeout: int = 120, poll_latency: float = 0.1
    ) -> TxReceipt:
        try:
            return wait_for_transaction_receipt(self.web3, transaction_hash, timeout, poll_latency)
        except Timeout:
            raise TimeExhausted(
                "Transaction {} is not in the chain, after {} seconds".format(
                    to_hex(transaction_hash),
                    timeout,
                )
            )

    get_transaction_receipt: Method[Callable[[_Hash32], TxReceipt]] = Method(
        RPC.platon_getTransactionReceipt,
        mungers=[default_root_munger]
    )

    get_transaction_count: Method[Callable[..., Nonce]] = Method(
        RPC.platon_getTransactionCount,
        mungers=[block_id_munger],
    )

    def replace_transaction(self, transaction_hash: _Hash32, new_transaction: TxParams) -> HexBytes:
        current_transaction = get_required_transaction(self.web3, transaction_hash)
        return replace_transaction(self.web3, current_transaction, new_transaction)

    def modify_transaction(
            self, transaction_hash: _Hash32, **transaction_params: Any
    ) -> HexBytes:
        assert_valid_transaction_params(cast(TxParams, transaction_params))
        current_transaction = get_required_transaction(self.web3, transaction_hash)
        current_transaction_params = extract_valid_transaction_params(current_transaction)
        new_transaction = merge(current_transaction_params, transaction_params)
        return replace_transaction(self.web3, current_transaction, new_transaction)

    def send_transaction(self, transaction: TxParams) -> HexBytes:
        return self._send_transaction(transaction)

    send_raw_transaction: Method[Callable[[Union[HexStr, bytes]], HexBytes]] = Method(
        RPC.platon_sendRawTransaction,
        mungers=[default_root_munger],
    )

    def sign_munger(
            self,
            account: Union[Address, Bech32Address, ENS],
            data: Union[int, bytes] = None,
            hexstr: HexStr = None,
            text: str = None
    ) -> Tuple[Union[Address, Bech32Address, ENS], HexStr]:
        message_hex = to_hex(data, hexstr=hexstr, text=text)
        return (account, message_hex)

    sign: Method[Callable[..., HexStr]] = Method(
        RPC.platon_sign,
        mungers=[sign_munger],
    )

    sign_transaction: Method[Callable[[TxParams], SignedTx]] = Method(
        RPC.platon_signTransaction,
        mungers=[default_root_munger],
    )

    sign_typed_data: Method[Callable[..., HexStr]] = Method(
        RPC.platon_signTypedData,
        mungers=[default_root_munger],
    )

    def call_munger(
            self,
            transaction: TxParams,
            block_identifier: Optional[BlockIdentifier] = None,
            state_override: Optional[CallOverrideParams] = None,
    ) -> Union[Tuple[TxParams, BlockIdentifier], Tuple[TxParams, BlockIdentifier, CallOverrideParams]]:
        # TODO: move to middleware
        if 'from' not in transaction and is_bech32_address(self.default_account):
            transaction = assoc(transaction, 'from', self.default_account)

        # TODO: move to middleware
        if block_identifier is None:
            block_identifier = self.default_block

        if state_override is None:
            return (transaction, block_identifier)
        else:
            return (transaction, block_identifier, state_override)

    call: Method[Callable[..., Union[bytes, bytearray]]] = Method(
        RPC.platon_call,
        mungers=[call_munger]
    )

    def estimate_gas(
            self,
            transaction: TxParams,
            block_identifier: Optional[BlockIdentifier] = None
    ) -> Von:
        return self._estimate_gas(transaction, block_identifier)

    def filter_munger(
            self,
            filter_params: Optional[Union[str, FilterParams]] = None,
            filter_id: Optional[HexStr] = None
    ) -> Union[List[FilterParams], List[HexStr], List[str]]:
        if filter_id and filter_params:
            raise TypeError(
                "Ambiguous invocation: provide either a `filter_params` or a `filter_id` argument. "
                "Both were supplied."
            )
        if isinstance(filter_params, dict):
            return [filter_params]
        elif is_string(filter_params):
            if filter_params in ['latest', 'pending']:
                return [filter_params]
            else:
                raise ValueError(
                    "The filter API only accepts the values of `pending` or "
                    "`latest` for string based filters"
                )
        elif filter_id and not filter_params:
            return [filter_id]
        else:
            raise TypeError("Must provide either filter_params as a string or "
                            "a valid filter object, or a filter_id as a string "
                            "or hex.")

    filter: Method[Callable[..., Any]] = Method(
        method_choice_depends_on_args=select_filter_method(
            if_new_block_filter=RPC.platon_newBlockFilter,
            if_new_pending_transaction_filter=RPC.platon_newPendingTransactionFilter,
            if_new_filter=RPC.platon_newFilter,
        ),
        mungers=[filter_munger],
    )

    get_filter_changes: Method[Callable[[HexStr], List[LogReceipt]]] = Method(
        RPC.platon_getFilterChanges,
        mungers=[default_root_munger]
    )

    get_filter_logs: Method[Callable[[HexStr], List[LogReceipt]]] = Method(
        RPC.platon_getFilterLogs,
        mungers=[default_root_munger]
    )

    get_logs: Method[Callable[[FilterParams], List[LogReceipt]]] = Method(
        RPC.platon_getLogs,
        mungers=[default_root_munger]
    )

    submit_work: Method[Callable[[int, _Hash32, _Hash32], bool]] = Method(
        RPC.platon_submitWork,
        mungers=[default_root_munger],
    )

    uninstall_filter: Method[Callable[[HexStr], bool]] = Method(
        RPC.platon_uninstallFilter,
        mungers=[default_root_munger],
    )

    @overload
    def contract(self, address: None = None, **kwargs: Any) -> Type[Contract]:
        ...

    @overload
    def contract(self, address: Union[Address, Bech32Address, ENS], **kwargs: Any) -> Contract:
        ...

    def contract(self,
                 address: Optional[Union[Address, Bech32Address, ENS]] = None,
                 **kwargs: Any
                 ) -> Union[Type[Contract], Contract]:

        ContractFactoryClass = kwargs.pop('ContractFactoryClass', self.defaultContractFactory)

        ContractFactory = ContractFactoryClass.factory(self.web3, **kwargs)

        if address:
            return ContractFactory(address)
        else:
            return ContractFactory

    def set_contract_factory(
            self, contractFactory: Type[Union[Contract, ConciseContract, ContractCaller]]
    ) -> None:
        self.defaultContractFactory = contractFactory

    get_work: Method[Callable[[], List[HexBytes]]] = Method(
        RPC.platon_getWork,
        mungers=None,
    )

    def generate_gas_price(self, transaction_params: Optional[TxParams] = None) -> Optional[Von]:
        return self._generate_gas_price(transaction_params)
