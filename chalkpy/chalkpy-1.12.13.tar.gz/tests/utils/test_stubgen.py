import os
import subprocess

import pytest

import chalk

try:
    import polars as pl
except ImportError:
    pl = None


@pytest.mark.skipif(pl is None, reason="Polars must be installed to generate all stubs")
def test_stubgen():
    """Test that the chalkpy stubgen runs and that the generated stub file is the one that is committed."""
    stub_file_path = os.path.join(
        os.path.dirname(chalk.__file__), "..", "typings", "chalk", "features", "feature_set_decorator.pyi"
    )
    with open(stub_file_path, "r") as f:
        current_stub_file = f.read()
    subprocess.check_call(["chalkpy", "stubgen"])
    with open(stub_file_path, "r") as f:
        new_stub_file = f.read()
    assert (
        current_stub_file == new_stub_file
    ), f"The typing stubs generated via `chalkpy stubgen` differ. Please re-run this command and commit the updated stub file at {os.path.abspath(stub_file_path)}"
