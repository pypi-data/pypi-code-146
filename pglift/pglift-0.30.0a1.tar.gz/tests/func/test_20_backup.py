import pytest

from pglift import instances, systemd
from pglift.ctx import Context
from pglift.models import system
from pglift.systemd import scheduler


@pytest.mark.usefixtures("require_systemd_scheduler", "require_pgbackrest")
def test_systemd_backup_job(ctx: Context, instance: system.Instance) -> None:
    unit = scheduler.unit("backup", instance.qualname)
    assert systemd.is_enabled(ctx, unit)
    assert systemd.is_active(ctx, unit)
    with instances.stopped(ctx, instance):
        assert not systemd.is_active(ctx, unit)
    assert systemd.is_active(ctx, unit)
