import subprocess

import pytest


@pytest.mark.parametrize(
    "module",
    ["instance", "dsn_info", "role", "database", "postgres_exporter"],
    ids=lambda v: f"module:{v}",
)
def test(module: str) -> None:
    subprocess.check_call(["ansible-doc", f"dalibo.pglift.{module}"])
