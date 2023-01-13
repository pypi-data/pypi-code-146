import logging
import os
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def setup_logger():
    logging.basicConfig(
        format="%(levelname)s %(name)s.%(funcName)s: %(message)s [%(filename)s:%(lineno)s]",
        force=True,
    )
    logging.getLogger("urllib3.connectionpool").setLevel("WARNING")
    logging.getLogger("ape").setLevel("ERROR")


@pytest.fixture(autouse=True)
def prevent_home_data_dir():
    home_ape = Path.home().resolve() / ".ape"
    cwd_ape = Path(".").resolve() / "ape"
    assert not home_ape.exists()
    assert not cwd_ape.exists()
    try:
        yield True
    finally:
        assert not home_ape.exists()
        assert not cwd_ape.exists()


@pytest.fixture
def txn_hash():
    return "0x96823521c0c1999e4c1023279a1b4ef343649d37ac5f5b50a5fc7264064cb0ac"


@pytest.fixture
def contract_address():
    return "0xbBeb16aB5F13cd52bDa5d7AD49be4E7677231680"


@pytest.fixture
def owner_address():
    return "0x27566e752e56D403fB436C8b7031e7fcc75b6b4f"


@pytest.fixture
def owner_private_key():
    return os.environ["TEST_ACCOUNT_PRIVATE_KEY"]
