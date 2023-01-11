# -*- coding: utf-8 -*-

import json
import math
import pytest
import time
from typing import (
    TYPE_CHECKING,
    Callable,
    Sequence,
    Union,
    cast,
)

from platon_typing import (
    BlockNumber,
    Bech32Address,
    HexAddress,
    HexStr,
)
from platon_utils import (
    is_boolean,
    is_bytes,
    is_bech32_address,
    is_dict,
    is_integer,
    is_list_like,
    is_same_address,
    is_string,
)
from hexbytes import (
    HexBytes,
)

from platon._utils.ens import (
    ens_addresses,
)
from platon.exceptions import (
    BlockNotFound,
    ContractLogicError,
    InvalidAddress,
    InvalidTransaction,
    NameNotFound,
    TransactionNotFound,
    TransactionTypeMismatch,
)
from platon.types import (
    BlockData,
    FilterParams,
    LogReceipt,
    Nonce,
    SyncStatus,
    TxParams,
    Von,
)

UNKNOWN_ADDRESS = Bech32Address(HexAddress(HexStr('0xdEADBEeF00000000000000000000000000000000')))
UNKNOWN_HASH = HexStr('0xdeadbeef00000000000000000000000000000000000000000000000000000000')

if TYPE_CHECKING:
    from platon import Web3
    from platon.contract import Contract


def mine_pending_block(web3: "Web3") -> None:
    timeout = 10

    web3.node.miner.start()  # type: ignore
    start = time.time()
    while time.time() < start + timeout:
        if len(web3.platon.get_block('pending')['transactions']) == 0:
            break
    web3.node.miner.stop()  # type: ignore


class AsyncPlatonModuleTest:
    @pytest.mark.asyncio
    async def test_platon_gas_price(self, async_w3: "Web3") -> None:
        gas_price = await async_w3.platon.gas_price  # type: ignore
        assert gas_price > 0

    @pytest.mark.asyncio
    async def test_isConnected(self, async_w3: "Web3") -> None:
        is_connected = await async_w3.isConnected()  # type: ignore
        assert is_connected is True

    @pytest.mark.asyncio
    async def test_platon_send_transaction_legacy(
        self, async_w3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
            'gasPrice': await async_w3.platon.gas_price,  # type: ignore
        }
        txn_hash = await async_w3.platon.send_transaction(txn_params)  # type: ignore
        txn = await async_w3.platon.get_transaction(txn_hash)  # type: ignore

        assert is_same_address(txn['from'], cast(Bech32Address, txn_params['from']))
        assert is_same_address(txn['to'], cast(Bech32Address, txn_params['to']))
        assert txn['value'] == 1
        assert txn['gas'] == 21000
        assert txn['gasPrice'] == txn_params['gasPrice']

    @pytest.mark.asyncio
    async def test_platon_send_transaction(
        self, async_w3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
            'maxFeePerGas': async_w3.toVon(3, 'gvon'),
            'maxPriorityFeePerGas': async_w3.toVon(1, 'gvon'),
        }
        txn_hash = await async_w3.platon.send_transaction(txn_params)  # type: ignore
        txn = await async_w3.platon.get_transaction(txn_hash)  # type: ignore

        assert is_same_address(txn['from'], cast(Bech32Address, txn_params['from']))
        assert is_same_address(txn['to'], cast(Bech32Address, txn_params['to']))
        assert txn['value'] == 1
        assert txn['gas'] == 21000
        assert txn['maxFeePerGas'] == txn_params['maxFeePerGas']
        assert txn['maxPriorityFeePerGas'] == txn_params['maxPriorityFeePerGas']
        assert txn['gasPrice'] is None

    @pytest.mark.asyncio
    async def test_platon_send_transaction_default_fees(
        self, async_w3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
        }
        txn_hash = await async_w3.platon.send_transaction(txn_params)  # type: ignore
        txn = await async_w3.platon.get_transaction(txn_hash)  # type: ignore

        assert is_same_address(txn['from'], cast(Bech32Address, txn_params['from']))
        assert is_same_address(txn['to'], cast(Bech32Address, txn_params['to']))
        assert txn['value'] == 1
        assert txn['gas'] == 21000
        assert txn['maxPriorityFeePerGas'] == 1 * 10**9
        assert txn['maxFeePerGas'] >= 1 * 10**9
        assert txn['gasPrice'] is None

    @pytest.mark.asyncio
    async def test_platon_send_transaction_hex_fees(
        self, async_w3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
            'maxFeePerGas': hex(250 * 10**9),
            'maxPriorityFeePerGas': hex(2 * 10**9),
        }
        txn_hash = await async_w3.platon.send_transaction(txn_params)  # type: ignore
        txn = await async_w3.platon.get_transaction(txn_hash)  # type: ignore

        assert is_same_address(txn['from'], cast(Bech32Address, txn_params['from']))
        assert is_same_address(txn['to'], cast(Bech32Address, txn_params['to']))
        assert txn['value'] == 1
        assert txn['gas'] == 21000
        assert txn['maxFeePerGas'] == 250 * 10**9
        assert txn['maxPriorityFeePerGas'] == 2 * 10**9

    @pytest.mark.asyncio
    async def test_platon_send_transaction_no_gas(
        self, async_w3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'maxFeePerGas': Von(250 * 10**9),
            'maxPriorityFeePerGas': Von(2 * 10**9),
        }
        txn_hash = await async_w3.platon.send_transaction(txn_params)  # type: ignore
        txn = await async_w3.platon.get_transaction(txn_hash)  # type: ignore

        assert is_same_address(txn['from'], cast(Bech32Address, txn_params['from']))
        assert is_same_address(txn['to'], cast(Bech32Address, txn_params['to']))
        assert txn['value'] == 1
        assert txn['gas'] == 121000  # 21000 + buffer

    @pytest.mark.asyncio
    async def test_platon_send_transaction_with_gas_price(
        self, async_w3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
            'gasPrice': Von(1),
            'maxFeePerGas': Von(250 * 10**9),
            'maxPriorityFeePerGas': Von(2 * 10**9),
        }
        with pytest.raises(TransactionTypeMismatch):
            await async_w3.platon.send_transaction(txn_params)  # type: ignore

    @pytest.mark.asyncio
    async def test_platon_send_transaction_no_priority_fee(
        self, async_w3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
            'maxFeePerGas': Von(250 * 10**9),
        }
        with pytest.raises(InvalidTransaction, match='maxPriorityFeePerGas must be defined'):
            await async_w3.platon.send_transaction(txn_params)  # type: ignore

    @pytest.mark.asyncio
    async def test_platon_send_transaction_no_max_fee(
        self, async_w3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        maxPriorityFeePerGas = async_w3.toVon(2, 'gvon')
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
            'maxPriorityFeePerGas': maxPriorityFeePerGas,
        }
        txn_hash = await async_w3.platon.send_transaction(txn_params)  # type: ignore
        txn = await async_w3.platon.get_transaction(txn_hash)  # type: ignore

        assert is_same_address(txn['from'], cast(Bech32Address, txn_params['from']))
        assert is_same_address(txn['to'], cast(Bech32Address, txn_params['to']))
        assert txn['value'] == 1
        assert txn['gas'] == 21000

        block = await async_w3.platon.get_block('latest')  # type: ignore
        assert txn['maxFeePerGas'] == maxPriorityFeePerGas + 2 * block['baseFeePerGas']

    @pytest.mark.asyncio
    async def test_platon_send_transaction_max_fee_less_than_tip(
        self, async_w3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
            'maxFeePerGas': Von(1 * 10**9),
            'maxPriorityFeePerGas': Von(2 * 10**9),
        }
        with pytest.raises(
            InvalidTransaction, match="maxFeePerGas must be >= maxPriorityFeePerGas"
        ):
            await async_w3.platon.send_transaction(txn_params)  # type: ignore

    @pytest.mark.asyncio
    async def test_gas_price_strategy_middleware(
        self, async_w3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
        }
        two_gvon_in_von = async_w3.toVon(2, 'gvon')

        def gas_price_strategy(web3: "Web3", txn: TxParams) -> Von:
            return two_gvon_in_von

        async_w3.platon.set_gas_price_strategy(gas_price_strategy)

        txn_hash = await async_w3.platon.send_transaction(txn_params)  # type: ignore
        txn = await async_w3.platon.get_transaction(txn_hash)  # type: ignore

        assert txn['gasPrice'] == two_gvon_in_von
        async_w3.platon.set_gas_price_strategy(None)  # reset strategy

    @pytest.mark.asyncio
    async def test_platon_estimate_gas(
        self, async_w3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        gas_estimate = await async_w3.platon.estimate_gas({  # type: ignore
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
        })
        assert is_integer(gas_estimate)
        assert gas_estimate > 0

    @pytest.mark.asyncio
    async def test_platon_getBlockByHash(
        self, async_w3: "Web3", empty_block: BlockData
    ) -> None:
        block = await async_w3.platon.get_block(empty_block['hash'])  # type: ignore
        assert block['hash'] == empty_block['hash']

    @pytest.mark.asyncio
    async def test_platon_getBlockByHash_not_found(self, async_w3: "Web3") -> None:
        with pytest.raises(BlockNotFound):
            await async_w3.platon.get_block(UNKNOWN_HASH)  # type: ignore

    @pytest.mark.asyncio
    async def test_platon_getBlockByHash_pending(
        self, async_w3: "Web3"
    ) -> None:
        block = await async_w3.platon.get_block('pending')  # type: ignore
        assert block['hash'] is None

    @pytest.mark.asyncio
    async def test_platon_getBlockByNumber_with_integer(
        self, async_w3: "Web3", empty_block: BlockData
    ) -> None:
        block = await async_w3.platon.get_block(empty_block['number'])  # type: ignore
        assert block['number'] == empty_block['number']

    @pytest.mark.asyncio
    async def test_platon_getBlockByNumber_latest(
        self, async_w3: "Web3", empty_block: BlockData
    ) -> None:
        current_block_number = await async_w3.platon.block_number  # type: ignore
        block = await async_w3.platon.get_block('latest')  # type: ignore
        assert block['number'] == current_block_number

    @pytest.mark.asyncio
    async def test_platon_getBlockByNumber_not_found(
        self, async_w3: "Web3", empty_block: BlockData
    ) -> None:
        with pytest.raises(BlockNotFound):
            await async_w3.platon.get_block(BlockNumber(12345))  # type: ignore

    @pytest.mark.asyncio
    async def test_platon_getBlockByNumber_pending(
        self, async_w3: "Web3", empty_block: BlockData
    ) -> None:
        current_block_number = await async_w3.platon.block_number  # type: ignore
        block = await async_w3.platon.get_block('pending')  # type: ignore
        assert block['number'] == current_block_number + 1

    @pytest.mark.asyncio
    async def test_platon_getBlockByNumber_earliest(
        self, async_w3: "Web3", empty_block: BlockData
    ) -> None:
        genesis_block = await async_w3.platon.get_block(BlockNumber(0))  # type: ignore
        block = await async_w3.platon.get_block('earliest')  # type: ignore
        assert block['number'] == 0
        assert block['hash'] == genesis_block['hash']

    @pytest.mark.asyncio
    async def test_platon_getBlockByNumber_full_transactions(
        self, async_w3: "Web3", block_with_txn: BlockData
    ) -> None:
        block = await async_w3.platon.get_block(block_with_txn['number'], True)  # type: ignore
        transaction = block['transactions'][0]
        assert transaction['hash'] == block_with_txn['transactions'][0]


class PlatonModuleTest:
    def test_platon_protocol_version(self, web3: "Web3") -> None:
        with pytest.warns(DeprecationWarning,
                          match="This method has been deprecated in some clients"):
            protocol_version = web3.platon.protocol_version

        assert is_string(protocol_version)
        assert protocol_version.isdigit()

    def test_platon_protocolVersion(self, web3: "Web3") -> None:
        with pytest.warns(DeprecationWarning):
            protocol_version = web3.platon.protocolVersion

        assert is_string(protocol_version)
        assert protocol_version.isdigit()

    def test_platon_syncing(self, web3: "Web3") -> None:
        syncing = web3.platon.syncing

        assert is_boolean(syncing) or is_dict(syncing)

        if is_boolean(syncing):
            assert syncing is False
        elif is_dict(syncing):
            sync_dict = cast(SyncStatus, syncing)
            assert 'startingBlock' in sync_dict
            assert 'currentBlock' in sync_dict
            assert 'highestBlock' in sync_dict

            assert is_integer(sync_dict['startingBlock'])
            assert is_integer(sync_dict['currentBlock'])
            assert is_integer(sync_dict['highestBlock'])

    def test_platon_coinbase(self, web3: "Web3") -> None:
        coinbase = web3.platon.coinbase
        assert is_bech32_address(coinbase)

    def test_platon_mining(self, web3: "Web3") -> None:
        mining = web3.platon.mining
        assert is_boolean(mining)

    def test_platon_hashrate(self, web3: "Web3") -> None:
        hashrate = web3.platon.hashrate
        assert is_integer(hashrate)
        assert hashrate >= 0

    def test_platon_chain_id(self, web3: "Web3") -> None:
        chain_id = web3.platon.chain_id
        # chain id value from node fixture genesis file
        assert chain_id == 131277322940537

    def test_platon_chainId(self, web3: "Web3") -> None:
        with pytest.warns(DeprecationWarning):
            chain_id = web3.platon.chainId
        # chain id value from node fixture genesis file
        assert chain_id == 131277322940537

    def test_platon_gas_price(self, web3: "Web3") -> None:
        gas_price = web3.platon.gas_price
        assert is_integer(gas_price)
        assert gas_price > 0

    def test_platon_accounts(self, web3: "Web3") -> None:
        accounts = web3.platon.accounts
        assert is_list_like(accounts)
        assert len(accounts) != 0
        assert all((
            is_bech32_address(account)
            for account
            in accounts
        ))
        assert web3.platon.coinbase in accounts

    def test_platon_block_number(self, web3: "Web3") -> None:
        block_number = web3.platon.block_number
        assert is_integer(block_number)
        assert block_number >= 0

    def test_platon_get_block_number(self, web3: "Web3") -> None:
        block_number = web3.platon.get_block_number()
        assert is_integer(block_number)
        assert block_number >= 0

    def test_platon_blockNumber(self, web3: "Web3") -> None:
        with pytest.warns(DeprecationWarning):
            block_number = web3.platon.blockNumber

        assert is_integer(block_number)
        assert block_number >= 0

    def test_platon_get_balance(self, web3: "Web3") -> None:
        coinbase = web3.platon.coinbase

        with pytest.raises(InvalidAddress):
            web3.platon.get_balance(Bech32Address(HexAddress(HexStr(coinbase.lower()))))

        balance = web3.platon.get_balance(coinbase)

        assert is_integer(balance)
        assert balance >= 0

    def test_platon_get_balance_with_block_identifier(self, web3: "Web3") -> None:
        miner_address = web3.platon.get_block(1)['miner']
        genesis_balance = web3.platon.get_balance(miner_address, 0)
        later_balance = web3.platon.get_balance(miner_address, 1)

        assert is_integer(genesis_balance)
        assert is_integer(later_balance)
        assert later_balance > genesis_balance

    @pytest.mark.parametrize('address, expect_success', [
        ('test-address.platon', True),
        ('not-an-address.platon', False)
    ])
    def test_platon_get_balance_with_ens_name(
        self, web3: "Web3", address: Bech32Address, expect_success: bool
    ) -> None:
        with ens_addresses(web3, {'test-address.platon': web3.platon.accounts[0]}):
            if expect_success:
                balance = web3.platon.get_balance(address)
                assert is_integer(balance)
                assert balance >= 0
            else:
                with pytest.raises(NameNotFound):
                    web3.platon.get_balance(address)

    def test_platon_get_storage_at(
        self, web3: "Web3", emitter_contract_address: Bech32Address
    ) -> None:
        storage = web3.platon.get_storage_at(emitter_contract_address, 0)
        assert isinstance(storage, HexBytes)

    def test_platon_get_storage_at_ens_name(
        self, web3: "Web3", emitter_contract_address: Bech32Address
    ) -> None:
        with ens_addresses(web3, {'emitter.platon': emitter_contract_address}):
            storage = web3.platon.get_storage_at('emitter.platon', 0)
            assert isinstance(storage, HexBytes)

    def test_platon_get_storage_at_invalid_address(self, web3: "Web3") -> None:
        coinbase = web3.platon.coinbase
        with pytest.raises(InvalidAddress):
            web3.platon.get_storage_at(Bech32Address(HexAddress(HexStr(coinbase.lower()))), 0)

    def test_platon_get_transaction_count(
        self, web3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        transaction_count = web3.platon.get_transaction_count(unlocked_account_dual_type)
        assert is_integer(transaction_count)
        assert transaction_count >= 0

    def test_platon_get_transaction_count_ens_name(
        self, web3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        with ens_addresses(web3, {'unlocked-acct-dual-type.platon': unlocked_account_dual_type}):
            transaction_count = web3.platon.get_transaction_count('unlocked-acct-dual-type.platon')
            assert is_integer(transaction_count)
            assert transaction_count >= 0

    def test_platon_get_transaction_count_invalid_address(self, web3: "Web3") -> None:
        coinbase = web3.platon.coinbase
        with pytest.raises(InvalidAddress):
            web3.platon.get_transaction_count(Bech32Address(HexAddress(HexStr(coinbase.lower()))))

    def test_platon_getBlockTransactionCountByHash_empty_block(
        self, web3: "Web3", empty_block: BlockData
    ) -> None:
        transaction_count = web3.platon.get_block_transaction_count(empty_block['hash'])

        assert is_integer(transaction_count)
        assert transaction_count == 0

    def test_platon_getBlockTransactionCountByNumber_empty_block(
        self, web3: "Web3", empty_block: BlockData
    ) -> None:
        transaction_count = web3.platon.get_block_transaction_count(empty_block['number'])

        assert is_integer(transaction_count)
        assert transaction_count == 0

    def test_platon_getBlockTransactionCountByHash_block_with_txn(
        self, web3: "Web3", block_with_txn: BlockData
    ) -> None:
        transaction_count = web3.platon.get_block_transaction_count(block_with_txn['hash'])

        assert is_integer(transaction_count)
        assert transaction_count >= 1

    def test_platon_getBlockTransactionCountByNumber_block_with_txn(
        self, web3: "Web3", block_with_txn: BlockData
    ) -> None:
        transaction_count = web3.platon.get_block_transaction_count(block_with_txn['number'])

        assert is_integer(transaction_count)
        assert transaction_count >= 1

    def test_platon_get_code(self, web3: "Web3", math_contract_address: Bech32Address) -> None:
        code = web3.platon.get_code(math_contract_address)
        assert isinstance(code, HexBytes)
        assert len(code) > 0

    def test_platon_get_code_ens_address(
        self, web3: "Web3", math_contract_address: Bech32Address
    ) -> None:
        with ens_addresses(
            web3, {'mathcontract.platon': math_contract_address}
        ):
            code = web3.platon.get_code('mathcontract.platon')
            assert isinstance(code, HexBytes)
            assert len(code) > 0

    def test_platon_get_code_invalid_address(self, web3: "Web3", math_contract: "Contract") -> None:
        with pytest.raises(InvalidAddress):
            web3.platon.get_code(Bech32Address(HexAddress(HexStr(math_contract.address.lower()))))

    def test_platon_get_code_with_block_identifier(
        self, web3: "Web3", emitter_contract: "Contract"
    ) -> None:
        code = web3.platon.get_code(emitter_contract.address, block_identifier=web3.platon.block_number)
        assert isinstance(code, HexBytes)
        assert len(code) > 0

    def test_platon_sign(self, web3: "Web3", unlocked_account_dual_type: Bech32Address) -> None:
        signature = web3.platon.sign(
            unlocked_account_dual_type, text='Message tö sign. Longer than hash!'
        )
        assert is_bytes(signature)
        assert len(signature) == 32 + 32 + 1

        # test other formats
        hexsign = web3.platon.sign(
            unlocked_account_dual_type,
            hexstr=HexStr(
                '0x4d6573736167652074c3b6207369676e2e204c6f6e676572207468616e206861736821'
            )
        )
        assert hexsign == signature

        intsign = web3.platon.sign(
            unlocked_account_dual_type,
            0x4d6573736167652074c3b6207369676e2e204c6f6e676572207468616e206861736821
        )
        assert intsign == signature

        bytessign = web3.platon.sign(
            unlocked_account_dual_type, b'Message t\xc3\xb6 sign. Longer than hash!'
        )
        assert bytessign == signature

        new_signature = web3.platon.sign(
            unlocked_account_dual_type, text='different message is different'
        )
        assert new_signature != signature

    def test_platon_sign_ens_names(
        self, web3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        with ens_addresses(web3, {'unlocked-acct.platon': unlocked_account_dual_type}):
            signature = web3.platon.sign(
                'unlocked-acct.platon', text='Message tö sign. Longer than hash!'
            )
            assert is_bytes(signature)
            assert len(signature) == 32 + 32 + 1

    def test_platon_sign_typed_data(
        self,
        web3: "Web3",
        unlocked_account_dual_type: Bech32Address,
        skip_if_testrpc: Callable[["Web3"], None],
    ) -> None:
        validJSONMessage = '''
            {
                "types": {
                    "EIP712Domain": [
                        {"name": "name", "type": "string"},
                        {"name": "version", "type": "string"},
                        {"name": "chain_id", "type": "uint256"},
                        {"name": "verifyingContract", "type": "address"}
                    ],
                    "Person": [
                        {"name": "name", "type": "string"},
                        {"name": "wallet", "type": "address"}
                    ],
                    "Mail": [
                        {"name": "from", "type": "Person"},
                        {"name": "to", "type": "Person"},
                        {"name": "contents", "type": "string"}
                    ]
                },
                "primaryType": "Mail",
                "domain": {
                    "name": "Ether Mail",
                    "version": "1",
                    "chain_id": "0x01",
                    "verifyingContract": "0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC"
                },
                "message": {
                    "from": {
                        "name": "Cow",
                        "wallet": "0xCD2a3d9F938E13CD947Ec05AbC7FE734Df8DD826"
                    },
                    "to": {
                        "name": "Bob",
                        "wallet": "0xbBbBBBBbbBBBbbbBbbBbbbbBBbBbbbbBbBbbBBbB"
                    },
                    "contents": "Hello, Bob!"
                }
            }
        '''
        skip_if_testrpc(web3)
        signature = HexBytes(web3.platon.sign_typed_data(
            unlocked_account_dual_type,
            json.loads(validJSONMessage)
        ))
        assert len(signature) == 32 + 32 + 1

    def test_invalid_platon_sign_typed_data(
        self,
        web3: "Web3",
        unlocked_account_dual_type: Bech32Address,
        skip_if_testrpc: Callable[["Web3"], None]
    ) -> None:
        skip_if_testrpc(web3)
        invalid_typed_message = '''
            {
                "types": {
                    "EIP712Domain": [
                        {"name": "name", "type": "string"},
                        {"name": "version", "type": "string"},
                        {"name": "chain_id", "type": "uint256"},
                        {"name": "verifyingContract", "type": "address"}
                    ],
                    "Person": [
                        {"name": "name", "type": "string"},
                        {"name": "wallet", "type": "address"}
                    ],
                    "Mail": [
                        {"name": "from", "type": "Person"},
                        {"name": "to", "type": "Person[2]"},
                        {"name": "contents", "type": "string"}
                    ]
                },
                "primaryType": "Mail",
                "domain": {
                    "name": "Ether Mail",
                    "version": "1",
                    "chain_id": "0x01",
                    "verifyingContract": "0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC"
                },
                "message": {
                    "from": {
                        "name": "Cow",
                        "wallet": "0xCD2a3d9F938E13CD947Ec05AbC7FE734Df8DD826"
                    },
                    "to": [{
                        "name": "Bob",
                        "wallet": "0xbBbBBBBbbBBBbbbBbbBbbbbBBbBbbbbBbBbbBBbB"
                    }],
                    "contents": "Hello, Bob!"
                }
            }
        '''
        with pytest.raises(ValueError,
                           match=r".*Expected 2 items for array type Person\[2\], got 1 items.*"):
            web3.platon.sign_typed_data(
                unlocked_account_dual_type,
                json.loads(invalid_typed_message)
            )

    def test_platon_sign_transaction(self, web3: "Web3", unlocked_account: Bech32Address) -> None:
        txn_params: TxParams = {
            'from': unlocked_account,
            'to': unlocked_account,
            'value': Von(1),
            'gas': Von(21000),
            'gasPrice': web3.platon.gas_price,
            'nonce': Nonce(0),
        }
        result = web3.platon.sign_transaction(txn_params)
        signatory_account = web3.platon.account.recover_transaction(result['raw'])
        assert unlocked_account == signatory_account
        assert result['tx']['to'] == txn_params['to']
        assert result['tx']['value'] == txn_params['value']
        assert result['tx']['gas'] == txn_params['gas']
        assert result['tx']['gasPrice'] == txn_params['gasPrice']
        assert result['tx']['nonce'] == txn_params['nonce']

    def test_platon_sign_transaction_ens_names(
        self, web3: "Web3", unlocked_account: Bech32Address
    ) -> None:
        with ens_addresses(web3, {'unlocked-account.platon': unlocked_account}):
            txn_params: TxParams = {
                'from': 'unlocked-account.platon',
                'to': 'unlocked-account.platon',
                'value': Von(1),
                'gas': Von(21000),
                'gasPrice': web3.platon.gas_price,
                'nonce': Nonce(0),
            }
            result = web3.platon.sign_transaction(txn_params)
            signatory_account = web3.platon.account.recover_transaction(result['raw'])
            assert unlocked_account == signatory_account
            assert result['tx']['to'] == unlocked_account
            assert result['tx']['value'] == txn_params['value']
            assert result['tx']['gas'] == txn_params['gas']
            assert result['tx']['gasPrice'] == txn_params['gasPrice']
            assert result['tx']['nonce'] == txn_params['nonce']

    def test_platon_send_transaction_addr_bech32_required(
        self, web3: "Web3", unlocked_account: Bech32Address
    ) -> None:
        non_bech32_addr = unlocked_account.lower()
        txn_params: TxParams = {
            'from': unlocked_account,
            'to': unlocked_account,
            'value': Von(1),
            'gas': Von(21000),
            'maxFeePerGas': web3.toVon(2, 'gvon'),
            'maxPriorityFeePerGas': web3.toVon(1, 'gvon'),
        }

        with pytest.raises(InvalidAddress):
            invalid_params = cast(TxParams, dict(txn_params, **{'from': non_bech32_addr}))
            web3.platon.send_transaction(invalid_params)

        with pytest.raises(InvalidAddress):
            invalid_params = cast(TxParams, dict(txn_params, **{'to': non_bech32_addr}))
            web3.platon.send_transaction(invalid_params)

    def test_platon_send_transaction_legacy(
        self, web3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
            'gasPrice': web3.platon.gas_price,
        }
        txn_hash = web3.platon.send_transaction(txn_params)
        txn = web3.platon.get_transaction(txn_hash)

        assert is_same_address(txn['from'], cast(Bech32Address, txn_params['from']))
        assert is_same_address(txn['to'], cast(Bech32Address, txn_params['to']))
        assert txn['value'] == 1
        assert txn['gas'] == 21000
        assert txn['gasPrice'] == txn_params['gasPrice']

    def test_platon_send_transaction(
        self, web3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
            'maxFeePerGas': web3.toVon(3, 'gvon'),
            'maxPriorityFeePerGas': web3.toVon(1, 'gvon'),
        }
        txn_hash = web3.platon.send_transaction(txn_params)
        txn = web3.platon.get_transaction(txn_hash)

        assert is_same_address(txn['from'], cast(Bech32Address, txn_params['from']))
        assert is_same_address(txn['to'], cast(Bech32Address, txn_params['to']))
        assert txn['value'] == 1
        assert txn['gas'] == 21000
        assert txn['maxFeePerGas'] == txn_params['maxFeePerGas']
        assert txn['maxPriorityFeePerGas'] == txn_params['maxPriorityFeePerGas']
        assert txn['gasPrice'] is None

    def test_platon_send_transaction_with_nonce(
        self, web3: "Web3", unlocked_account: Bech32Address
    ) -> None:
        mine_pending_block(web3)  # gives an accurate transaction count after mining

        txn_params: TxParams = {
            'from': unlocked_account,
            'to': unlocked_account,
            'value': Von(1),
            'gas': Von(21000),
            # unique maxFeePerGas to ensure transaction hash different from other tests
            'maxFeePerGas': web3.toVon(4.321, 'gvon'),
            'maxPriorityFeePerGas': web3.toVon(1, 'gvon'),
            'nonce': web3.platon.get_transaction_count(unlocked_account),
        }
        txn_hash = web3.platon.send_transaction(txn_params)
        txn = web3.platon.get_transaction(txn_hash)

        assert is_same_address(txn['from'], cast(Bech32Address, txn_params['from']))
        assert is_same_address(txn['to'], cast(Bech32Address, txn_params['to']))
        assert txn['value'] == 1
        assert txn['gas'] == 21000
        assert txn['maxFeePerGas'] == txn_params['maxFeePerGas']
        assert txn['maxPriorityFeePerGas'] == txn_params['maxPriorityFeePerGas']
        assert txn['nonce'] == txn_params['nonce']
        assert txn['gasPrice'] is None

    def test_platon_send_transaction_default_fees(
        self, web3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
        }
        txn_hash = web3.platon.send_transaction(txn_params)
        txn = web3.platon.get_transaction(txn_hash)

        assert is_same_address(txn['from'], cast(Bech32Address, txn_params['from']))
        assert is_same_address(txn['to'], cast(Bech32Address, txn_params['to']))
        assert txn['value'] == 1
        assert txn['gas'] == 21000
        assert txn['maxPriorityFeePerGas'] == 1 * 10**9
        assert txn['maxFeePerGas'] >= 1 * 10**9
        assert txn['gasPrice'] is None

    def test_platon_send_transaction_hex_fees(
        self, web3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
            'maxFeePerGas': hex(250 * 10**9),
            'maxPriorityFeePerGas': hex(2 * 10**9),
        }
        txn_hash = web3.platon.send_transaction(txn_params)
        txn = web3.platon.get_transaction(txn_hash)

        assert is_same_address(txn['from'], cast(Bech32Address, txn_params['from']))
        assert is_same_address(txn['to'], cast(Bech32Address, txn_params['to']))
        assert txn['value'] == 1
        assert txn['gas'] == 21000
        assert txn['maxFeePerGas'] == 250 * 10**9
        assert txn['maxPriorityFeePerGas'] == 2 * 10**9

    def test_platon_send_transaction_no_gas(
        self, web3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'maxFeePerGas': Von(250 * 10**9),
            'maxPriorityFeePerGas': Von(2 * 10**9),
        }
        txn_hash = web3.platon.send_transaction(txn_params)
        txn = web3.platon.get_transaction(txn_hash)

        assert is_same_address(txn['from'], cast(Bech32Address, txn_params['from']))
        assert is_same_address(txn['to'], cast(Bech32Address, txn_params['to']))
        assert txn['value'] == 1
        assert txn['gas'] == 121000  # 21000 + buffer

    def test_platon_send_transaction_with_gas_price(
        self, web3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
            'gasPrice': Von(1),
            'maxFeePerGas': Von(250 * 10**9),
            'maxPriorityFeePerGas': Von(2 * 10**9),
        }
        with pytest.raises(TransactionTypeMismatch):
            web3.platon.send_transaction(txn_params)

    def test_platon_send_transaction_no_priority_fee(
        self, web3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
            'maxFeePerGas': Von(250 * 10**9),
        }
        with pytest.raises(InvalidTransaction, match='maxPriorityFeePerGas must be defined'):
            web3.platon.send_transaction(txn_params)

    def test_platon_send_transaction_no_max_fee(
        self, web3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        maxPriorityFeePerGas = web3.toVon(2, 'gvon')
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
            'maxPriorityFeePerGas': maxPriorityFeePerGas,
        }
        txn_hash = web3.platon.send_transaction(txn_params)
        txn = web3.platon.get_transaction(txn_hash)

        assert is_same_address(txn['from'], cast(Bech32Address, txn_params['from']))
        assert is_same_address(txn['to'], cast(Bech32Address, txn_params['to']))
        assert txn['value'] == 1
        assert txn['gas'] == 21000

        block = web3.platon.get_block('latest')
        assert txn['maxFeePerGas'] == maxPriorityFeePerGas + 2 * block['baseFeePerGas']

    def test_platon_send_transaction_max_fee_less_than_tip(
        self, web3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
            'maxFeePerGas': Von(1 * 10**9),
            'maxPriorityFeePerGas': Von(2 * 10**9),
        }
        with pytest.raises(
            InvalidTransaction, match="maxFeePerGas must be >= maxPriorityFeePerGas"
        ):
            web3.platon.send_transaction(txn_params)

    def test_platon_replace_transaction_legacy(
        self, web3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
            'gasPrice': web3.platon.gas_price,
        }
        txn_hash = web3.platon.send_transaction(txn_params)

        txn_params['gasPrice'] = Von(web3.platon.gas_price * 2)
        replace_txn_hash = web3.platon.replace_transaction(txn_hash, txn_params)
        replace_txn = web3.platon.get_transaction(replace_txn_hash)

        assert is_same_address(replace_txn['from'], cast(Bech32Address, txn_params['from']))
        assert is_same_address(replace_txn['to'], cast(Bech32Address, txn_params['to']))
        assert replace_txn['value'] == 1
        assert replace_txn['gas'] == 21000
        assert replace_txn['gasPrice'] == txn_params['gasPrice']

    def test_platon_replace_transaction(
        self, web3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        two_gvon_in_von = web3.toVon(2, 'gvon')
        three_gvon_in_von = web3.toVon(3, 'gvon')

        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
            'maxFeePerGas': two_gvon_in_von,
            'maxPriorityFeePerGas': web3.toVon(1, 'gvon'),
        }
        txn_hash = web3.platon.send_transaction(txn_params)

        txn_params['maxFeePerGas'] = three_gvon_in_von
        txn_params['maxPriorityFeePerGas'] = two_gvon_in_von

        replace_txn_hash = web3.platon.replace_transaction(txn_hash, txn_params)
        replace_txn = web3.platon.get_transaction(replace_txn_hash)

        assert is_same_address(replace_txn['from'], cast(Bech32Address, txn_params['from']))
        assert is_same_address(replace_txn['to'], cast(Bech32Address, txn_params['to']))
        assert replace_txn['value'] == 1
        assert replace_txn['gas'] == 21000
        assert replace_txn['maxFeePerGas'] == three_gvon_in_von
        assert replace_txn['maxPriorityFeePerGas'] == two_gvon_in_von

    def test_platon_replace_transaction_underpriced(
        self, web3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
            'maxFeePerGas': web3.toVon(3, 'gvon'),
            'maxPriorityFeePerGas': web3.toVon(2, 'gvon'),
        }
        txn_hash = web3.platon.send_transaction(txn_params)

        one_gvon_in_von = web3.toVon(1, 'gvon')
        txn_params['maxFeePerGas'] = one_gvon_in_von
        txn_params['maxPriorityFeePerGas'] = one_gvon_in_von

        with pytest.raises(ValueError, match="replacement transaction underpriced"):
            web3.platon.replace_transaction(txn_hash, txn_params)

    def test_platon_replace_transaction_non_existing_transaction(
        self, web3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
            'maxFeePerGas': web3.toVon(3, 'gvon'),
            'maxPriorityFeePerGas': web3.toVon(1, 'gvon'),
        }
        with pytest.raises(TransactionNotFound):
            web3.platon.replace_transaction(
                HexStr('0x98e8cc09b311583c5079fa600f6c2a3bea8611af168c52e4b60b5b243a441997'),
                txn_params
            )

    def test_platon_replace_transaction_already_mined(
        self, web3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
            'maxFeePerGas': web3.toVon(2, 'gvon'),
            'maxPriorityFeePerGas': web3.toVon(1, 'gvon'),
        }
        txn_hash = web3.platon.send_transaction(txn_params)
        try:
            web3.node.miner.start()  # type: ignore
            web3.platon.wait_for_transaction_receipt(txn_hash, timeout=10)
        finally:
            web3.node.miner.stop()  # type: ignore

        txn_params['maxFeePerGas'] = web3.toVon(3, 'gvon')
        txn_params['maxPriorityFeePerGas'] = web3.toVon(2, 'gvon')
        with pytest.raises(ValueError, match="Supplied transaction with hash"):
            web3.platon.replace_transaction(txn_hash, txn_params)

    def test_platon_replace_transaction_incorrect_nonce(
        self, web3: "Web3", unlocked_account: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account,
            'to': unlocked_account,
            'value': Von(1),
            'gas': Von(21000),
            'maxFeePerGas': web3.toVon(2, 'gvon'),
            'maxPriorityFeePerGas': web3.toVon(1, 'gvon'),
        }
        txn_hash = web3.platon.send_transaction(txn_params)
        txn = web3.platon.get_transaction(txn_hash)

        txn_params['maxFeePerGas'] = web3.toVon(3, 'gvon')
        txn_params['maxPriorityFeePerGas'] = web3.toVon(2, 'gvon')
        txn_params['nonce'] = Nonce(txn['nonce'] + 1)
        with pytest.raises(ValueError):
            web3.platon.replace_transaction(txn_hash, txn_params)

    def test_platon_replace_transaction_gas_price_too_low(
        self, web3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
            'gasPrice': web3.toVon(2, 'gvon'),
        }
        txn_hash = web3.platon.send_transaction(txn_params)

        txn_params['gasPrice'] = web3.toVon(1, 'gvon')
        with pytest.raises(ValueError):
            web3.platon.replace_transaction(txn_hash, txn_params)

    def test_platon_replace_transaction_gas_price_defaulting_minimum(
        self, web3: "Web3", unlocked_account: Bech32Address
    ) -> None:
        gas_price = web3.toVon(1, 'gvon')

        txn_params: TxParams = {
            'from': unlocked_account,
            'to': unlocked_account,
            'value': Von(1),
            'gas': Von(21000),
            'gasPrice': gas_price,
        }
        txn_hash = web3.platon.send_transaction(txn_params)

        txn_params.pop('gasPrice')
        replace_txn_hash = web3.platon.replace_transaction(txn_hash, txn_params)
        replace_txn = web3.platon.get_transaction(replace_txn_hash)

        assert replace_txn['gasPrice'] == math.ceil(gas_price * 1.125)  # minimum gas price

    def test_platon_replace_transaction_gas_price_defaulting_strategy_higher(
        self, web3: "Web3", unlocked_account: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account,
            'to': unlocked_account,
            'value': Von(1),
            'gas': Von(21000),
            'gasPrice': web3.toVon(1, 'gvon'),
        }
        txn_hash = web3.platon.send_transaction(txn_params)

        two_gvon_in_von = web3.toVon(2, 'gvon')

        def higher_gas_price_strategy(web3: "Web3", txn: TxParams) -> Von:
            return two_gvon_in_von

        web3.platon.set_gas_price_strategy(higher_gas_price_strategy)

        txn_params.pop('gasPrice')
        replace_txn_hash = web3.platon.replace_transaction(txn_hash, txn_params)
        replace_txn = web3.platon.get_transaction(replace_txn_hash)
        assert replace_txn['gasPrice'] == two_gvon_in_von  # Strategy provides higher gas price
        web3.platon.set_gas_price_strategy(None)  # reset strategy

    def test_platon_replace_transaction_gas_price_defaulting_strategy_lower(
        self, web3: "Web3", unlocked_account: Bech32Address
    ) -> None:
        gas_price = web3.toVon(2, 'gvon')

        txn_params: TxParams = {
            'from': unlocked_account,
            'to': unlocked_account,
            'value': Von(1),
            'gas': Von(21000),
            'gasPrice': gas_price,
        }
        txn_hash = web3.platon.send_transaction(txn_params)

        def lower_gas_price_strategy(web3: "Web3", txn: TxParams) -> Von:
            return web3.toVon(1, 'gvon')

        web3.platon.set_gas_price_strategy(lower_gas_price_strategy)

        txn_params.pop('gasPrice')
        replace_txn_hash = web3.platon.replace_transaction(txn_hash, txn_params)
        replace_txn = web3.platon.get_transaction(replace_txn_hash)
        # Strategy provides lower gas price - minimum preferred
        assert replace_txn['gasPrice'] == math.ceil(gas_price * 1.125)
        web3.platon.set_gas_price_strategy(None)  # reset strategy

    def test_platon_modify_transaction_legacy(
        self, web3: "Web3", unlocked_account: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account,
            'to': unlocked_account,
            'value': Von(1),
            'gas': Von(21000),
            'gasPrice': web3.platon.gas_price,
        }
        txn_hash = web3.platon.send_transaction(txn_params)

        modified_txn_hash = web3.platon.modify_transaction(
            txn_hash, gasPrice=(cast(int, txn_params['gasPrice']) * 2), value=2
        )
        modified_txn = web3.platon.get_transaction(modified_txn_hash)

        assert is_same_address(modified_txn['from'], cast(Bech32Address, txn_params['from']))
        assert is_same_address(modified_txn['to'], cast(Bech32Address, txn_params['to']))
        assert modified_txn['value'] == 2
        assert modified_txn['gas'] == 21000
        assert modified_txn['gasPrice'] == cast(int, txn_params['gasPrice']) * 2

    def test_platon_modify_transaction(
        self, web3: "Web3", unlocked_account: Bech32Address
    ) -> None:
        txn_params: TxParams = {
            'from': unlocked_account,
            'to': unlocked_account,
            'value': Von(1),
            'gas': Von(21000),
            'maxPriorityFeePerGas': web3.toVon(1, 'gvon'),
            'maxFeePerGas': web3.toVon(2, 'gvon'),
        }
        txn_hash = web3.platon.send_transaction(txn_params)

        modified_txn_hash = web3.platon.modify_transaction(
            txn_hash,
            value=2,
            maxPriorityFeePerGas=(cast(Von, txn_params['maxPriorityFeePerGas']) * 2),
            maxFeePerGas=(cast(Von, txn_params['maxFeePerGas']) * 2),
        )
        modified_txn = web3.platon.get_transaction(modified_txn_hash)

        assert is_same_address(modified_txn['from'], cast(Bech32Address, txn_params['from']))
        assert is_same_address(modified_txn['to'], cast(Bech32Address, txn_params['to']))
        assert modified_txn['value'] == 2
        assert modified_txn['gas'] == 21000
        assert modified_txn['maxPriorityFeePerGas'] == cast(Von, txn_params[
            'maxPriorityFeePerGas']) * 2
        assert modified_txn['maxFeePerGas'] == cast(Von, txn_params['maxFeePerGas']) * 2

    @pytest.mark.parametrize(
        'raw_transaction, expected_hash',
        [
            (
                # private key 0x3c2ab4e8f17a7dea191b8c991522660126d681039509dc3bb31af7c9bdb63518
                # This is an unfunded account, but the transaction has a 0 gas price, so is valid.
                # It never needs to be mined, we just want the transaction hash back to confirm.
                # tx = {'to': '0x0000000000000000000000000000000000000000', 'value': 0, 'nonce': 0, 'gas': 21000, 'gasPrice': 0, 'chainId': 131277322940537}
                HexBytes('0xf8658080825208940000000000000000000000000000000000000000808086eecac466e115a038176e5f9f1c25ce470ce77856bacbc02dd728ad647bb8b18434ac62c3e8e14fa03279bb3ee1e5202580668ec62b66a7d01355de3d5c4ef18fcfcb88fac56d5f90'),
                '0x6ab943e675003de610b4e94f2e289dc711688df6e150da2bc57bd03811ad0f63',
            ),
        ]
    )
    def test_platon_send_raw_transaction(
        self,
        web3: "Web3",
        raw_transaction: Union[HexStr, bytes],
        funded_account_for_raw_txn: Bech32Address,
        expected_hash: HexStr,
    ) -> None:
        txn_hash = web3.platon.send_raw_transaction(raw_transaction)
        assert txn_hash == web3.toBytes(hexstr=expected_hash)

    def test_platon_call(
        self, web3: "Web3", math_contract: "Contract"
    ) -> None:
        coinbase = web3.platon.coinbase
        txn_params = math_contract._prepare_transaction(
            fn_name='add',
            fn_args=(7, 11),
            transaction={'from': coinbase, 'to': math_contract.address},
        )
        call_result = web3.platon.call(txn_params)
        assert is_string(call_result)
        result = web3.codec.decode_single('uint256', call_result)
        assert result == 18

    def test_platon_call_with_override(
        self, web3: "Web3", revert_contract: "Contract"
    ) -> None:
        coinbase = web3.platon.coinbase
        txn_params = revert_contract._prepare_transaction(
            fn_name='normalFunction',
            transaction={'from': coinbase, 'to': revert_contract.address},
        )
        call_result = web3.platon.call(txn_params)
        result = web3.codec.decode_single('bool', call_result)
        assert result is True

        # override runtime bytecode: `normalFunction` returns `false`
        override_code = '0x6080604052348015600f57600080fd5b5060043610603c5760003560e01c8063185c38a4146041578063c06a97cb146049578063d67e4b84146051575b600080fd5b60476071565b005b604f60df565b005b605760e4565b604051808215151515815260200191505060405180910390f35b6040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252601b8152602001807f46756e6374696f6e20686173206265656e2072657665727465642e000000000081525060200191505060405180910390fd5b600080fd5b60008090509056fea2646970667358221220bb71e9e9a2e271cd0fbe833524a3ea67df95f25ea13aef5b0a761fa52b538f1064736f6c63430006010033'
        call_result = web3.platon.call(
            txn_params,
            'latest',
            {revert_contract.address: {'code': override_code}}
        )
        result = web3.codec.decode_single('bool', call_result)
        assert result is False

    def test_platon_call_with_0_result(
        self, web3: "Web3", math_contract: "Contract"
    ) -> None:
        coinbase = web3.platon.coinbase
        txn_params = math_contract._prepare_transaction(
            fn_name='add',
            fn_args=(0, 0),
            transaction={'from': coinbase, 'to': math_contract.address},
        )
        call_result = web3.platon.call(txn_params)
        assert is_string(call_result)
        result = web3.codec.decode_single('uint256', call_result)
        assert result == 0

    def test_platon_call_revert_with_msg(
        self,
        web3: "Web3",
        revert_contract: "Contract",
        unlocked_account: Bech32Address,
    ) -> None:
        with pytest.raises(ContractLogicError,
                           match='execution reverted: Function has been reverted'):
            txn_params = revert_contract._prepare_transaction(
                fn_name="revertWithMessage",
                transaction={
                    "from": unlocked_account,
                    "to": revert_contract.address,
                },
            )
            web3.platon.call(txn_params)

    def test_platon_call_revert_without_msg(
        self,
        web3: "Web3",
        revert_contract: "Contract",
        unlocked_account: Bech32Address,
    ) -> None:
        with pytest.raises(ContractLogicError, match="execution reverted"):
            txn_params = revert_contract._prepare_transaction(
                fn_name="revertWithoutMessage",
                transaction={
                    "from": unlocked_account,
                    "to": revert_contract.address,
                },
            )
            web3.platon.call(txn_params)

    def test_platon_estimate_gas_revert_with_msg(
        self,
        web3: "Web3",
        revert_contract: "Contract",
        unlocked_account: Bech32Address,
    ) -> None:
        with pytest.raises(ContractLogicError,
                           match='execution reverted: Function has been reverted'):
            txn_params = revert_contract._prepare_transaction(
                fn_name="revertWithMessage",
                transaction={
                    "from": unlocked_account,
                    "to": revert_contract.address,
                },
            )
            web3.platon.estimate_gas(txn_params)

    def test_platon_estimate_gas_revert_without_msg(
        self,
        web3: "Web3",
        revert_contract: "Contract",
        unlocked_account: Bech32Address,
    ) -> None:
        with pytest.raises(ContractLogicError, match="execution reverted"):
            txn_params = revert_contract._prepare_transaction(
                fn_name="revertWithoutMessage",
                transaction={
                    "from": unlocked_account,
                    "to": revert_contract.address,
                },
            )
            web3.platon.estimate_gas(txn_params)

    def test_platon_estimate_gas(
        self, web3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        gas_estimate = web3.platon.estimate_gas({
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
        })
        assert is_integer(gas_estimate)
        assert gas_estimate > 0

    def test_platon_estimate_gas_with_block(
        self, web3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        gas_estimate = web3.platon.estimate_gas({
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
        }, 'latest')
        assert is_integer(gas_estimate)
        assert gas_estimate > 0

    def test_platon_getBlockByHash(
        self, web3: "Web3", empty_block: BlockData
    ) -> None:
        block = web3.platon.get_block(empty_block['hash'])
        assert block['hash'] == empty_block['hash']

    def test_platon_getBlockByHash_not_found(
        self, web3: "Web3", empty_block: BlockData
    ) -> None:
        with pytest.raises(BlockNotFound):
            web3.platon.get_block(UNKNOWN_HASH)

    def test_platon_getBlockByHash_pending(
        self, web3: "Web3"
    ) -> None:
        block = web3.platon.get_block('pending')
        assert block['hash'] is None

    def test_platon_getBlockByNumber_with_integer(
        self, web3: "Web3", empty_block: BlockData
    ) -> None:
        block = web3.platon.get_block(empty_block['number'])
        assert block['number'] == empty_block['number']

    def test_platon_getBlockByNumber_latest(
        self, web3: "Web3", empty_block: BlockData
    ) -> None:
        current_block_number = web3.platon.block_number
        block = web3.platon.get_block('latest')
        assert block['number'] == current_block_number

    def test_platon_getBlockByNumber_not_found(
        self, web3: "Web3", empty_block: BlockData
    ) -> None:
        with pytest.raises(BlockNotFound):
            web3.platon.get_block(BlockNumber(12345))

    def test_platon_getBlockByNumber_pending(
        self, web3: "Web3", empty_block: BlockData
    ) -> None:
        current_block_number = web3.platon.block_number
        block = web3.platon.get_block('pending')
        assert block['number'] == current_block_number + 1

    def test_platon_getBlockByNumber_earliest(
        self, web3: "Web3", empty_block: BlockData
    ) -> None:
        genesis_block = web3.platon.get_block(BlockNumber(0))
        block = web3.platon.get_block('earliest')
        assert block['number'] == 0
        assert block['hash'] == genesis_block['hash']

    def test_platon_getBlockByNumber_full_transactions(
        self, web3: "Web3", block_with_txn: BlockData
    ) -> None:
        block = web3.platon.get_block(block_with_txn['number'], True)
        transaction = block['transactions'][0]
        assert transaction['hash'] == block_with_txn['transactions'][0]  # type: ignore

    def test_platon_getTransactionByHash(
        self, web3: "Web3", mined_txn_hash: HexStr
    ) -> None:
        transaction = web3.platon.get_transaction(mined_txn_hash)
        assert is_dict(transaction)
        assert transaction['hash'] == HexBytes(mined_txn_hash)

    def test_platon_getTransactionByHash_contract_creation(
        self, web3: "Web3", math_contract_deploy_txn_hash: HexStr
    ) -> None:
        transaction = web3.platon.get_transaction(math_contract_deploy_txn_hash)
        assert is_dict(transaction)
        assert transaction['to'] is None, "to field is %r" % transaction['to']

    def test_platon_getTransactionByBlockHashAndIndex(
        self, web3: "Web3", block_with_txn: BlockData, mined_txn_hash: HexStr
    ) -> None:
        transaction = web3.platon.get_transaction_by_block(block_with_txn['hash'], 0)
        assert is_dict(transaction)
        assert transaction['hash'] == HexBytes(mined_txn_hash)

    def test_platon_getTransactionByBlockNumberAndIndex(
        self, web3: "Web3", block_with_txn: BlockData, mined_txn_hash: HexStr
    ) -> None:
        transaction = web3.platon.get_transaction_by_block(block_with_txn['number'], 0)
        assert is_dict(transaction)
        assert transaction['hash'] == HexBytes(mined_txn_hash)

    def test_platon_get_transaction_receipt_mined(
        self, web3: "Web3", block_with_txn: BlockData, mined_txn_hash: HexStr
    ) -> None:
        receipt = web3.platon.get_transaction_receipt(mined_txn_hash)
        assert is_dict(receipt)
        assert receipt['blockNumber'] == block_with_txn['number']
        assert receipt['blockHash'] == block_with_txn['hash']
        assert receipt['transactionIndex'] == 0
        assert receipt['transactionHash'] == HexBytes(mined_txn_hash)
        assert is_bech32_address(receipt['to'])
        assert receipt['from'] is not None
        assert is_bech32_address(receipt['from'])

    def test_platon_get_transaction_receipt_unmined(
        self, web3: "Web3", unlocked_account_dual_type: Bech32Address
    ) -> None:
        txn_hash = web3.platon.send_transaction({
            'from': unlocked_account_dual_type,
            'to': unlocked_account_dual_type,
            'value': Von(1),
            'gas': Von(21000),
            'maxFeePerGas': web3.toVon(3, 'gvon'),
            'maxPriorityFeePerGas': web3.toVon(1, 'gvon')
        })
        with pytest.raises(TransactionNotFound):
            web3.platon.get_transaction_receipt(txn_hash)

    def test_platon_get_transaction_receipt_with_log_entry(
        self,
        web3: "Web3",
        block_with_txn_with_log: BlockData,
        emitter_contract: "Contract",
        txn_hash_with_log: HexStr,
    ) -> None:
        receipt = web3.platon.get_transaction_receipt(txn_hash_with_log)
        assert is_dict(receipt)
        assert receipt['blockNumber'] == block_with_txn_with_log['number']
        assert receipt['blockHash'] == block_with_txn_with_log['hash']
        assert receipt['transactionIndex'] == 0
        assert receipt['transactionHash'] == HexBytes(txn_hash_with_log)

        assert len(receipt['logs']) == 1
        log_entry = receipt['logs'][0]

        assert log_entry['blockNumber'] == block_with_txn_with_log['number']
        assert log_entry['blockHash'] == block_with_txn_with_log['hash']
        assert log_entry['logIndex'] == 0
        assert is_same_address(log_entry['address'], emitter_contract.address)
        assert log_entry['transactionIndex'] == 0
        assert log_entry['transactionHash'] == HexBytes(txn_hash_with_log)

    def test_platon_newFilter(self, web3: "Web3") -> None:
        filter = web3.platon.filter({})

        changes = web3.platon.get_filter_changes(filter.filter_id)
        assert is_list_like(changes)
        assert not changes

        logs = web3.platon.get_filter_logs(filter.filter_id)
        assert is_list_like(logs)
        assert not logs

        result = web3.platon.uninstall_filter(filter.filter_id)
        assert result is True

    def test_platon_newBlockFilter(self, web3: "Web3") -> None:
        filter = web3.platon.filter('latest')
        assert is_string(filter.filter_id)

        changes = web3.platon.get_filter_changes(filter.filter_id)
        assert is_list_like(changes)
        assert not changes

        # TODO: figure out why this fails in platon
        # logs = platon.platon.get_filter_logs(filter.filter_id)
        # assert is_list_like(logs)
        # assert not logs

        result = web3.platon.uninstall_filter(filter.filter_id)
        assert result is True

    def test_platon_newPendingTransactionFilter(self, web3: "Web3") -> None:
        filter = web3.platon.filter('pending')
        assert is_string(filter.filter_id)

        changes = web3.platon.get_filter_changes(filter.filter_id)
        assert is_list_like(changes)
        assert not changes

        # TODO: figure out why this fails in platon
        # logs = platon.platon.get_filter_logs(filter.filter_id)
        # assert is_list_like(logs)
        # assert not logs

        result = web3.platon.uninstall_filter(filter.filter_id)
        assert result is True

    def test_platon_get_logs_without_logs(
        self, web3: "Web3", block_with_txn_with_log: BlockData
    ) -> None:
        # Test with block range

        filter_params: FilterParams = {
            "fromBlock": BlockNumber(0),
            "toBlock": BlockNumber(block_with_txn_with_log['number'] - 1),
        }
        result = web3.platon.get_logs(filter_params)
        assert len(result) == 0

        # the range is wrong
        filter_params = {
            "fromBlock": block_with_txn_with_log['number'],
            "toBlock": BlockNumber(block_with_txn_with_log['number'] - 1),
        }
        result = web3.platon.get_logs(filter_params)
        assert len(result) == 0

        # Test with `address`

        # filter with other address
        filter_params = {
            "fromBlock": BlockNumber(0),
            "address": UNKNOWN_ADDRESS,
        }
        result = web3.platon.get_logs(filter_params)
        assert len(result) == 0

        # Test with multiple `address`

        # filter with other address
        filter_params = {
            "fromBlock": BlockNumber(0),
            "address": [UNKNOWN_ADDRESS, UNKNOWN_ADDRESS],
        }
        result = web3.platon.get_logs(filter_params)
        assert len(result) == 0

    def test_platon_get_logs_with_logs(
        self,
        web3: "Web3",
        block_with_txn_with_log: BlockData,
        emitter_contract_address: Bech32Address,
        txn_hash_with_log: HexStr,
    ) -> None:
        def assert_contains_log(result: Sequence[LogReceipt]) -> None:
            assert len(result) == 1
            log_entry = result[0]
            assert log_entry['blockNumber'] == block_with_txn_with_log['number']
            assert log_entry['blockHash'] == block_with_txn_with_log['hash']
            assert log_entry['logIndex'] == 0
            assert is_same_address(log_entry['address'], emitter_contract_address)
            assert log_entry['transactionIndex'] == 0
            assert log_entry['transactionHash'] == HexBytes(txn_hash_with_log)

        # Test with block range

        # the range includes the block where the log resides in
        filter_params: FilterParams = {
            "fromBlock": block_with_txn_with_log['number'],
            "toBlock": block_with_txn_with_log['number'],
        }
        result = web3.platon.get_logs(filter_params)
        assert_contains_log(result)

        # specify only `from_block`. by default `to_block` should be 'latest'
        filter_params = {
            "fromBlock": BlockNumber(0),
        }
        result = web3.platon.get_logs(filter_params)
        assert_contains_log(result)

        # Test with `address`

        # filter with emitter_contract.address
        filter_params = {
            "fromBlock": BlockNumber(0),
            "address": emitter_contract_address,
        }

    def test_platon_get_logs_with_logs_topic_args(
        self,
        web3: "Web3",
        block_with_txn_with_log: BlockData,
        emitter_contract_address: Bech32Address,
        txn_hash_with_log: HexStr,
    ) -> None:
        def assert_contains_log(result: Sequence[LogReceipt]) -> None:
            assert len(result) == 1
            log_entry = result[0]
            assert log_entry['blockNumber'] == block_with_txn_with_log['number']
            assert log_entry['blockHash'] == block_with_txn_with_log['hash']
            assert log_entry['logIndex'] == 0
            assert is_same_address(log_entry['address'], emitter_contract_address)
            assert log_entry['transactionIndex'] == 0
            assert log_entry['transactionHash'] == HexBytes(txn_hash_with_log)

        # Test with None event sig

        filter_params: FilterParams = {
            "fromBlock": BlockNumber(0),
            "topics": [
                None,
                HexStr('0x000000000000000000000000000000000000000000000000000000000000d431')],
        }

        result = web3.platon.get_logs(filter_params)
        assert_contains_log(result)

        # Test with None indexed arg
        filter_params = {
            "fromBlock": BlockNumber(0),
            "topics": [
                HexStr('0x057bc32826fbe161da1c110afcdcae7c109a8b69149f727fc37a603c60ef94ca'),
                None],
        }
        result = web3.platon.get_logs(filter_params)
        assert_contains_log(result)

    def test_platon_get_logs_with_logs_none_topic_args(self, web3: "Web3") -> None:
        # Test with None overflowing
        filter_params: FilterParams = {
            "fromBlock": BlockNumber(0),
            "topics": [None, None, None],
        }

        result = web3.platon.get_logs(filter_params)
        assert len(result) == 0

    def test_platon_call_old_contract_state(
        self, web3: "Web3", math_contract: "Contract", unlocked_account: Bech32Address
    ) -> None:
        start_block = web3.platon.get_block('latest')
        block_num = start_block["number"]
        block_hash = start_block["hash"]

        math_contract.functions.increment().transact({'from': unlocked_account})

        # This isn't an incredibly convincing test since we can't mine, and
        # the default resolved block is latest, So if block_identifier was ignored
        # we would get the same result. For now, we mostly depend on core tests.
        # Ideas to improve this test:
        #  - Enable on-demand mining in more clients
        #  - Increment the math contract in all of the fixtures, and check the value in an old block
        block_hash_call_result = math_contract.functions.counter().call(block_identifier=block_hash)
        block_num_call_result = math_contract.functions.counter().call(block_identifier=block_num)
        latest_call_result = math_contract.functions.counter().call(block_identifier='latest')
        default_call_result = math_contract.functions.counter().call()
        pending_call_result = math_contract.functions.counter().call(block_identifier='pending')

        assert block_hash_call_result == 0
        assert block_num_call_result == 0
        assert latest_call_result == 0
        assert default_call_result == 0

        if pending_call_result != 1:
            raise AssertionError("pending call result was %d instead of 1" % pending_call_result)

    def test_platon_uninstall_filter(self, web3: "Web3") -> None:
        filter = web3.platon.filter({})
        assert is_string(filter.filter_id)

        success = web3.platon.uninstall_filter(filter.filter_id)
        assert success is True

        failure = web3.platon.uninstall_filter(filter.filter_id)
        assert failure is False

    def test_platon_getTransactionFromBlock_deprecation(
        self, web3: "Web3", block_with_txn: BlockData
    ) -> None:
        with pytest.raises(DeprecationWarning):
            web3.platon.getTransactionFromBlock(block_with_txn['hash'], 0)

    def test_platon_getCompilers_deprecation(self, web3: "Web3") -> None:
        with pytest.raises(DeprecationWarning):
            web3.platon.getCompilers()

    def test_platon_submit_hashrate(self, web3: "Web3") -> None:
        # node_id from EIP 1474: https://github.com/platonnetwork/EIPs/pull/1474/files
        node_id = HexStr('59daa26581d0acd1fce254fb7e85952f4c09d0915afd33d3886cd914bc7d283c')
        result = web3.platon.submit_hashrate(5000, node_id)
        assert result is True

    def test_platon_submit_work(self, web3: "Web3") -> None:
        nonce = 1
        pow_hash = HexStr('0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef')
        mix_digest = HexStr('0xD1FE5700000000000000000000000000D1FE5700000000000000000000000000')
        result = web3.platon.submit_work(nonce, pow_hash, mix_digest)
        assert result is False
