from typing import Any
from typing import Dict
from typing import List
from unittest import mock

import pytest
from dict_tools.data import NamespaceDict


# ================================================================================
# pop fixtures
# ================================================================================
@pytest.fixture(scope="session", autouse=True)
def acct_subs() -> List[str]:
    return ["{{cookiecutter.service_name}}"]


@pytest.fixture(scope="session", autouse=True)
def acct_profile() -> str:
    # The name of the profile that will be used for tests
    # Do NOT use production credentials for tests!
    # A profile with this name needs to be defined in the $ACCT_FILE in order to run these tests
    return "test_development_idem_{{cookiecutter.service_name}}"


@pytest.fixture(scope="session", name="hub")
def integration_hub(hub):
    hub.pop.sub.add(dyne_name="idem")

    with mock.patch("sys.argv", ["idem", "state"]):
        hub.pop.config.load(["idem", "acct"], "idem", parse_cli=True)

    yield hub


async def _setup_hub(hub):
    # Set up the hub before each function here
    ...


async def _teardown_hub(hub):
    # Clean up the hub after each function here
    ...


@pytest.fixture(scope="function", autouse=True)
async def function_hub_wrapper(hub):
    await _setup_hub(hub)
    yield
    await _teardown_hub(hub)


@pytest.mark.asyncio
@pytest.fixture(scope="module")
async def ctx(hub, acct_subs: List[str], acct_profile: str) -> Dict[str, Any]:
    ctx = NamespaceDict(run_name="test", test=False)

    if not hub.OPT.acct.acct_file:
        pytest.skip(
            "Missing acct_file.  "
            "Add ACCT_FILE to your environment with the path to your encrypted credentials file"
        )
    if not hub.OPT.acct.acct_file:
        pytest.skip(
            "Missing acct_key.  "
            "Add ACCT_KEY to your environment with the fernet key to decrypt your credentials file"
        )

    # Add the profile to the account
    await hub.acct.init.unlock(hub.OPT.acct.acct_file, hub.OPT.acct.acct_key)
    if not hub.acct.UNLOCKED:
        pytest.skip(f"acct could not unlock {hub.OPT.acct.acct_file}")
    ctx.acct = await hub.acct.init.gather(acct_subs, acct_profile)

    # Test if the created ctx is functional; if not then skip all the integration tests that use it
    if not ctx.acct.get("connection"):
        pytest.skip("ctx is not configured correctly")

    yield ctx

    # Close all connections when the tests are complete
    await hub.acct.init.close()


# --------------------------------------------------------------------------------
