from typing import Iterator

from pglift import postgresql, roles
from pglift.ctx import Context
from pglift.models import interface, system

from . import reconfigure_instance, role_in_pgpass


def test_instance_port_changed(
    ctx: Context,
    instance_manifest: interface.Instance,
    instance: system.Instance,
    tmp_port_factory: Iterator[int],
) -> None:
    """Check that change of instance port is reflected in password file
    entries.
    """
    role1, role2, role3 = (
        interface.Role(name="r1", password="1", pgpass=True),
        interface.Role(name="r2", password="2", pgpass=True),
        interface.Role(name="r3", pgpass=False),
    )
    surole = instance_manifest.surole(ctx.settings)
    assert postgresql.is_running(ctx, instance)
    roles.apply(ctx, instance, role1)
    roles.apply(ctx, instance, role2)
    roles.apply(ctx, instance, role3)
    port = instance.port
    passfile = ctx.settings.postgresql.auth.passfile
    assert role_in_pgpass(passfile, role1, port=port)
    assert role_in_pgpass(passfile, role2, port=port)
    assert not role_in_pgpass(passfile, role3)
    if surole.pgpass:
        assert role_in_pgpass(passfile, surole, port=port)
    newport = next(tmp_port_factory)
    with reconfigure_instance(ctx, instance_manifest, port=newport):
        assert not role_in_pgpass(passfile, role1, port=port)
        assert role_in_pgpass(passfile, role1, port=newport)
        assert not role_in_pgpass(passfile, role2, port=port)
        assert role_in_pgpass(passfile, role2, port=newport)
        assert not role_in_pgpass(passfile, role3)
        if surole.pgpass:
            assert not role_in_pgpass(passfile, surole, port=port)
            assert role_in_pgpass(passfile, surole, port=newport)
