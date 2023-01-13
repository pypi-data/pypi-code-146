import pytest

@pytest.fixture(scope="session")
def tmp_datasets_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("data")