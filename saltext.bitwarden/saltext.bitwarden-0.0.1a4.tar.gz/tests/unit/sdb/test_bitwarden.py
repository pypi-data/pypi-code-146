import pytest
import saltext.bitwarden.sdb.bitwarden_mod as bitwarden_sdb


@pytest.fixture
def configure_loader_modules():
    module_globals = {
        "__salt__": {"this_does_not_exist.please_replace_it": lambda: True},
    }
    return {
        bitwarden_sdb: module_globals,
    }


def test_replace_this_this_with_something_meaningful():
    assert "this_does_not_exist.please_replace_it" in bitwarden_sdb.__salt__
    assert bitwarden_sdb.__salt__["this_does_not_exist.please_replace_it"]() is True
