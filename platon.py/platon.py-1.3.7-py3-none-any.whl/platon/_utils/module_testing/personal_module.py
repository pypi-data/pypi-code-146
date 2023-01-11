import json
import pytest
from typing import (
    TYPE_CHECKING,
    cast,
)

from platon_typing import (
    Bech32Address,
)
from platon_utils import (
    is_bech32_address,
    is_list_like,
    is_same_address,
    is_string,
)
from hexbytes import (
    HexBytes,
)

from platon.types import (
    TxParams,
    Von,
)

if TYPE_CHECKING:
    from platon import Web3

PRIVATE_KEY_HEX = '0x56ebb41875ceedd42e395f730e03b5c44989393c9f0484ee6bc05f933673458f'
SECOND_PRIVATE_KEY_HEX = '0x56ebb41875ceedd42e395f730e03b5c44989393c9f0484ee6bc05f9336712345'
PASSWORD = 'platon-testing'
ADDRESS = '0x844B417c0C58B02c2224306047B9fb0D3264fE8c'
SECOND_ADDRESS = '0xB96b6B21053e67BA59907E252D990C71742c41B8'


PRIVATE_KEY_FOR_UNLOCK = '0x392f63a79b1ff8774845f3fa69de4a13800a59e7083f5187f1558f0797ad0f01'
ACCOUNT_FOR_UNLOCK = '0x12efDc31B1a8FA1A1e756DFD8A1601055C971E13'


class GoPlatonPersonalModuleTest:
    def test_personal_import_raw_key(self, web3: "Web3") -> None:
        actual = web3.node.personal.import_raw_key(PRIVATE_KEY_HEX, PASSWORD)
        assert actual == ADDRESS

    def test_personal_list_accounts(self, web3: "Web3") -> None:
        accounts = web3.node.personal.list_accounts()
        assert is_list_like(accounts)
        assert len(accounts) > 0
        assert all((
            is_bech32_address(item)
            for item
            in accounts
        ))

    def test_personal_list_wallets(self, web3: "Web3") -> None:
        wallets = web3.node.personal.list_wallets()
        assert is_list_like(wallets)
        assert len(wallets) > 0
        assert is_bech32_address(wallets[0]['accounts'][0]['address'])
        assert is_string(wallets[0]['accounts'][0]['url'])
        assert is_string(wallets[0]['status'])
        assert is_string(wallets[0]['url'])

    def test_personal_lock_account(
        self, web3: "Web3", unlockable_account_dual_type: Bech32Address
    ) -> None:
        # TODO: how do we test this better?
        web3.node.personal.lock_account(unlockable_account_dual_type)

    def test_personal_unlock_account_success(
        self,
        web3: "Web3",
        unlockable_account_dual_type: Bech32Address,
        unlockable_account_pw: str,
    ) -> None:
        result = web3.node.personal.unlock_account(
            unlockable_account_dual_type,
            unlockable_account_pw
        )
        assert result is True

    def test_personal_unlock_account_failure(
        self, web3: "Web3", unlockable_account_dual_type: Bech32Address
    ) -> None:
        with pytest.raises(ValueError):
            web3.node.personal.unlock_account(unlockable_account_dual_type, 'bad-password')

    def test_personal_send_transaction(
        self,
        web3: "Web3",
        unlockable_account_dual_type: Bech32Address,
        unlockable_account_pw: str,
    ) -> None:
        assert web3.platon.get_balance(unlockable_account_dual_type) > web3.toVon(1, 'ether')
        txn_params: TxParams = {
            'from': unlockable_account_dual_type,
            'to': unlockable_account_dual_type,
            'gas': Von(21000),
            'value': Von(1),
            'gasPrice': web3.toVon(1, 'benefit'),
        }
        txn_hash = web3.node.personal.send_transaction(txn_params, unlockable_account_pw)
        assert txn_hash
        transaction = web3.platon.get_transaction(txn_hash)

        assert is_same_address(transaction['from'], cast(Bech32Address, txn_params['from']))
        assert is_same_address(transaction['to'], cast(Bech32Address, txn_params['to']))
        assert transaction['gas'] == txn_params['gas']
        assert transaction['value'] == txn_params['value']
        assert transaction['gasPrice'] == txn_params['gasPrice']

    def test_personal_sign_and_ecrecover(
        self,
        web3: "Web3",
        unlockable_account_dual_type: Bech32Address,
        unlockable_account_pw: str,
    ) -> None:
        message = 'test-platon-node-personal-sign'
        signature = web3.node.personal.sign(
            message,
            unlockable_account_dual_type,
            unlockable_account_pw
        )
        signer = web3.node.personal.ec_recover(message, signature)
        assert is_same_address(signer, unlockable_account_dual_type)

    @pytest.mark.xfail(
        reason="personal_sign_typed_data JSON RPC call has not been released in node"
    )
    def test_personal_sign_typed_data(
        self,
        web3: "Web3",
        unlockable_account_dual_type: Bech32Address,
        unlockable_account_pw: str,
    ) -> None:
        typed_message = '''
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
        signature = HexBytes(web3.node.personal.sign_typed_data(
            json.loads(typed_message),
            unlockable_account_dual_type,
            unlockable_account_pw
        ))

        expected_signature = HexBytes(
            "0xc8b56aaeefd10ab4005c2455daf28d9082af661ac347cd"
            "b612d5b5e11f339f2055be831bf57a6e6cb5f6d93448fa35"
            "c1bd56fe1d745ffa101e74697108668c401c"
        )
        assert signature == expected_signature
        assert len(signature) == 32 + 32 + 1


class ParityPersonalModuleTest():

    def test_personal_list_accounts(self, web3: "Web3") -> None:
        accounts = web3.parity.personal.list_accounts()
        assert is_list_like(accounts)
        assert len(accounts) > 0
        assert all((
            is_bech32_address(item)
            for item
            in accounts
        ))

    def test_personal_unlock_account_success(
        self,
        web3: "Web3",
        unlockable_account_dual_type: Bech32Address,
        unlockable_account_pw: str,
    ) -> None:
        result = web3.parity.personal.unlock_account(
            unlockable_account_dual_type,
            unlockable_account_pw,
            None
        )
        assert result is True

    # Seems to be an issue with Parity since this should return False
    def test_personal_unlock_account_failure(
        self,
        web3: "Web3",
        unlockable_account_dual_type: Bech32Address,
    ) -> None:
        result = web3.parity.personal.unlock_account(
            unlockable_account_dual_type,
            'bad-password',
            None
        )
        assert result is True

    def test_personal_new_account(self, web3: "Web3") -> None:
        new_account = web3.parity.personal.new_account(PASSWORD)
        assert is_bech32_address(new_account)

    @pytest.mark.xfail(reason='this non-standard json-rpc method is not implemented on parity')
    def test_personal_lock_account(
        self, web3: "Web3", unlocked_account: Bech32Address
    ) -> None:
        # method undefined in superclass
        super().test_personal_lock_account(web3, unlocked_account)  # type: ignore

    @pytest.mark.xfail(reason='this non-standard json-rpc method is not implemented on parity')
    def test_personal_import_raw_key(self, web3: "Web3") -> None:
        # method undefined in superclass
        super().test_personal_import_raw_key(web3)  # type: ignore

    def test_personal_send_transaction(
        self,
        web3: "Web3",
        unlockable_account_dual_type: Bech32Address,
        unlockable_account_pw: str,
    ) -> None:
        assert web3.platon.get_balance(unlockable_account_dual_type) > web3.toVon(1, 'ether')
        txn_params: TxParams = {
            'from': unlockable_account_dual_type,
            'to': unlockable_account_dual_type,
            'gas': Von(21000),
            'value': Von(1),
            'gasPrice': web3.toVon(1, 'gvon'),
        }
        txn_hash = web3.parity.personal.send_transaction(txn_params, unlockable_account_pw)
        assert txn_hash
        transaction = web3.platon.get_transaction(txn_hash)

        assert is_same_address(transaction['from'], cast(Bech32Address, txn_params['from']))
        assert is_same_address(transaction['to'], cast(Bech32Address, txn_params['to']))
        assert transaction['gas'] == txn_params['gas']
        assert transaction['value'] == txn_params['value']
        assert transaction['gasPrice'] == txn_params['gasPrice']

    def test_personal_sign_and_ecrecover(
        self,
        web3: "Web3",
        unlockable_account_dual_type: Bech32Address,
        unlockable_account_pw: str,
    ) -> None:
        message = 'test-platon-parity-personal-sign'
        signature = web3.parity.personal.sign(
            message,
            unlockable_account_dual_type,
            unlockable_account_pw
        )
        signer = web3.parity.personal.ec_recover(message, signature)
        assert is_same_address(signer, unlockable_account_dual_type)

    def test_personal_sign_typed_data(
        self,
        web3: "Web3",
        unlockable_account_dual_type: Bech32Address,
        unlockable_account_pw: str,
    ) -> None:
        typed_message = '''
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
        signature = HexBytes(web3.parity.personal.sign_typed_data(
            json.loads(typed_message),
            unlockable_account_dual_type,
            unlockable_account_pw
        ))

        expected_signature = HexBytes(
            "0xc8b56aaeefd10ab4005c2455daf28d9082af661ac347cd"
            "b612d5b5e11f339f2055be831bf57a6e6cb5f6d93448fa35"
            "c1bd56fe1d745ffa101e74697108668c401c"
        )
        assert signature == expected_signature
        assert len(signature) == 32 + 32 + 1

    def test_invalid_personal_sign_typed_data(
        self,
        web3: "Web3",
        unlockable_account_dual_type: Bech32Address,
        unlockable_account_pw: str,
    ) -> None:
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
            web3.parity.personal.sign_typed_data(
                json.loads(invalid_typed_message),
                unlockable_account_dual_type,
                unlockable_account_pw
            )
