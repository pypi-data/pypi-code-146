# contract call tests

import logging
from pprint import pformat

import pytest
from eth_utils import to_wei

import ape_apeman
from ape_apeman.context import ContractCallResult

info = logging.info

TIP_GWEI = 10


@pytest.fixture
def ape():
    with ape_apeman.wrangler() as ape:
        yield ape


def test_call_lookup(ape, contract_address):
    contract = ape.Contract(contract_address)
    symbol = contract.symbol()
    assert symbol == "ETHERSIEVE"


@pytest.mark.tryfirst
def test_call_set(ape, contract_address, owner_address, owner_private_key):
    royalty_fee = 1000000000000000
    result = ape.call_contract(
        contract_address,
        "setPrintRoyalty",
        royalty_fee,
        private_key=owner_private_key,
        max_priority_fee=ape.provider.priority_fee + to_wei(TIP_GWEI, "gwei"),
    )
    assert isinstance(result, ContractCallResult)
    info(pformat(result.ret))
    info(pformat(result.receipt))


def test_call_get_set(ape, contract_address, owner_address, owner_private_key):
    # get the current prices
    pre_prices = ape.call_contract(
        contract_address, "getPrices", sender=owner_address
    )
    info(f"{pre_prices=}")
    assert pre_prices.ret.printRoyalty == 1000000000000000
    assert pre_prices.receipt is None

    # set the royalty price
    ret_set = ape.call_contract(
        contract_address,
        "setPrintRoyalty",
        13337,
        sender=owner_address,
        private_key=owner_private_key,
        autosign=True,
        max_priority_fee=ape.provider.priority_fee + to_wei(TIP_GWEI, "gwei"),
    )
    assert ret_set.ret is None
    assert ret_set.receipt

    # get the changed price
    tmp_prices = ape.call_contract(
        contract_address, "getPrices", sender=owner_address
    )
    info(f"{tmp_prices=}")
    assert tmp_prices.ret.printRoyalty == 13337
    assert tmp_prices.receipt is None

    # reset the price back to the original value
    ret_reset = ape.call_contract(
        contract_address,
        "setPrintRoyalty",
        pre_prices.ret.printRoyalty,
        private_key=owner_private_key,
        autosign=True,
        max_priority_fee=ape.provider.priority_fee + to_wei(TIP_GWEI, "gwei"),
    )
    assert ret_reset.ret is None
    assert ret_reset.receipt

    # finally test that the price is restored to original value
    post_prices = ape.call_contract(
        contract_address, "getPrices", sender=owner_address
    )
    info(f"{post_prices=}")
    assert post_prices.ret.printRoyalty == pre_prices.ret.printRoyalty
    assert post_prices.receipt is None


def test_call_mint(ape, contract_address, owner_address, owner_private_key):
    uri = "ipfs://bafkreie5npehcwbdbog3j4w7otw22jzm6szsjtihtjnhc5oxhvwukhczgm"
    result = ape.call_contract(
        contract_address,
        "safeMint",
        owner_address,
        uri,
        private_key=owner_private_key,
        max_priority_fee=ape.provider.priority_fee + to_wei(TIP_GWEI, "gwei"),
    )
    assert isinstance(result, ContractCallResult)
    info(pformat(result.dict()))
