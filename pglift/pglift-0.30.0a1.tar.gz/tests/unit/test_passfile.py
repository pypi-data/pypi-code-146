from pathlib import Path

import pytest

from pglift import passfile as passfile_mod
from pglift.ctx import Context
from pglift.models.system import Instance

from .test_roles import Role


@pytest.fixture
def passfile(ctx: Context) -> Path:
    fpath = ctx.settings.postgresql.auth.passfile
    fpath.write_text("*:999:*:edgar:fbi\n")
    return fpath


@pytest.mark.parametrize(
    "role, changed, pgpass",
    [
        (Role("alice"), False, "*:999:*:edgar:fbi\n"),
        (Role("bob", "secret"), False, "*:999:*:edgar:fbi\n"),
        (Role("charles", pgpass=True), False, "*:999:*:edgar:fbi\n"),
        (Role("danny", "sss", True), True, "*:999:*:danny:sss\n*:999:*:edgar:fbi\n"),
        (Role("edgar", "cia", True), True, "*:999:*:edgar:cia\n"),
        (Role("edgar", None, False), True, ""),
    ],
)
def test_role_change(
    ctx: Context,
    instance: Instance,
    passfile: Path,
    role: Role,
    changed: bool,
    pgpass: str,
) -> None:
    assert passfile_mod.role_change(ctx=ctx, instance=instance, role=role) == changed
    assert passfile.read_text() == pgpass
