# test use from python code

import logging
from pathlib import Path
from pprint import pformat
from subprocess import run

import pytest
from ape.exceptions import ContractLogicError
from ape_ethereum.transactions import Receipt
from eth_account import Account
from eth_utils import is_same_address

import ape_apeman.context

info = logging.info


@pytest.fixture
def APE(monkeypatch, shared_datadir):
    monkeypatch.setenv("APE_PROJECT_DIR", str(shared_datadir / "ape_project"))
    monkeypatch.setenv("APE_DATA_DIR", str(shared_datadir / "ape_data"))
    return ape_apeman.context.APE


@pytest.fixture
def check_url():
    def _check_url(url):
        assert isinstance(url, str)
        assert url.startswith("https://")

    return _check_url


@pytest.fixture
def check_receipt():
    def _check_receipt(receipt):
        assert isinstance(receipt, Receipt)

    return _check_receipt


@pytest.fixture
def check_block_number():
    def _check_block_number(block_number):
        assert isinstance(block_number, int)
        assert block_number > 1

    return _check_block_number


def test_module_context_url(APE, txn_hash, check_url):
    with APE() as ape:
        url = ape.explorer.get_transaction_url(txn_hash)
    check_url(url)


def test_module_init_url(APE, txn_hash, check_url):
    ape = APE(connect=True)
    url = ape.explorer.get_transaction_url(txn_hash)
    check_url(url)


def test_module_connect_url(APE, txn_hash, check_url):
    ape = APE()
    ape.connect()
    url = ape.explorer.get_transaction_url(txn_hash)
    check_url(url)


def test_module_context_receipt(APE, txn_hash, check_receipt):
    with APE() as ape:
        receipt = ape.provider.get_receipt(txn_hash)
    check_receipt(receipt)


def test_module_init_receipt(APE, txn_hash, check_receipt):
    ape = APE(connect=True)
    receipt = ape.provider.get_receipt(txn_hash)
    check_receipt(receipt)


def test_module_connect_receipt(APE, txn_hash, check_receipt):
    ape = APE()
    ape.connect()
    receipt = ape.provider.get_receipt(txn_hash)
    check_receipt(receipt)


def test_module_context_web3(APE, check_block_number):
    with APE() as ape:
        n = ape.web3.eth.get_block_number()
    check_block_number(n)


def test_module_init_web3(APE, check_block_number):
    ape = APE(connect=True)
    n = ape.web3.eth.get_block_number()
    check_block_number(n)


def test_module_connect_web3(APE, check_block_number):
    ape = APE()
    ape.connect()
    n = ape.web3.eth.get_block_number()
    check_block_number(n)


def test_module_context_contract(APE, contract_address):
    with APE() as ape:
        contract = ape.contracts.instance_at(contract_address)
        assert contract
        symbol = contract.symbol()
        assert symbol == "ETHERSIEVE"
        print(f"{contract_address=} {symbol=}")


def test_module_init_contract(APE, contract_address):
    ape = APE(connect=True)
    contract = ape.contracts.instance_at(contract_address)
    assert contract
    symbol = contract.symbol()
    assert symbol == "ETHERSIEVE"
    print(f"{contract_address=} {symbol=}")


def test_module_connect_contract(APE, contract_address):
    ape = APE()
    ape.connect()
    contract = ape.contracts.instance_at(contract_address)
    assert contract
    symbol = contract.symbol()
    assert symbol == "ETHERSIEVE"
    print(f"{contract_address=} {symbol=}")


def _sign_and_send(ape, contract_address, owner_address, owner_private_key):
    account = Account().from_key(owner_private_key)
    assert account.address == owner_address
    contract = ape.Contract(contract_address)
    nonce_before = ape.provider.get_nonce(account.address)
    txn = contract.getPrices.as_transaction(
        sender=account.address,
        required_confirmations=1,
        max_priority_fee="10 gwei",
    )
    txn.nonce = ape.provider.get_nonce(account.address)
    txn.signature = account.sign_transaction(txn.dict())
    receipt = ape.provider.send_transaction(txn)
    print(receipt)
    ret = receipt.return_value
    print(ret)
    nonce_after = ape.provider.get_nonce(account.address)
    assert nonce_before != nonce_after


@pytest.mark.uses_gas
def test_module_context_sign_and_send(
    APE, contract_address, owner_address, owner_private_key
):
    with APE() as ape:
        _sign_and_send(ape, contract_address, owner_address, owner_private_key)


@pytest.mark.uses_gas
def test_module_init_sign_and_send(
    APE, contract_address, owner_address, owner_private_key
):
    ape = APE(connect=True)
    _sign_and_send(ape, contract_address, owner_address, owner_private_key)


@pytest.mark.uses_gas
def test_module_connect_sign_and_send(
    APE, contract_address, owner_address, owner_private_key
):
    ape = APE()
    ape.connect()
    _sign_and_send(ape, contract_address, owner_address, owner_private_key)


def pdebug(object):
    logging.debug(pformat(object))


def _find_files(dir, label=None, output=pdebug):
    dir = Path(dir).resolve()
    label = label or str(dir)
    proc = run(
        ["find", str(dir), "-type", "f"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert not proc.stderr
    files = proc.stdout.strip().split("\n")
    if output:
        output({label: files})
    return files


def test_module_account_call(
    APE, shared_datadir, contract_address, owner_address, owner_private_key
):
    with APE() as ape:
        # call a public function

        contract = ape.Contract(contract_address)
        symbol = contract.symbol()
        assert symbol == "ETHERSIEVE"

        # call a function requiring authorized caller address
        with pytest.raises(ContractLogicError) as exc:
            components = contract.getComponents()
        assert exc
        assert "is missing role" in str(exc.value)

        # specify the public address in the lookup
        components = contract.getComponents(sender=owner_address)
        assert components

        # create an ape account
        account = ape.account(private_key=owner_private_key)
        assert is_same_address(account.address, owner_address)

        # with account.autosign_enabled():
        components = contract.getComponents(sender=account.address)
        assert components

        prices = contract.getPrices(sender=account.address)
        assert prices

        with account:
            prices = contract.getPrices(sender=account.address)
        assert prices

        with account.autosign_enabled():
            prices = contract.getPrices(sender=account.address)
        assert prices

        info(pformat(components))
        info(pformat(prices))
