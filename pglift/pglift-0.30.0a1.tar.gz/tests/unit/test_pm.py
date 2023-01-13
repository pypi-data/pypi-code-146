from pglift import pm, settings


def test_pluginmanager_all() -> None:
    p = pm.PluginManager.all()
    assert {name for name, _ in p.list_name_plugin()} == {
        "pglift.backup",
        "pglift.databases",
        "pglift.instances",
        "pglift.passfile",
        "pglift.patroni",
        "pglift.pgbackrest",
        "pglift.pgbackrest.repo_host",
        "pglift.pgbackrest.repo_path",
        "pglift.postgresql",
        "pglift.powa",
        "pglift.prometheus",
        "pglift.systemd.scheduler",
        "pglift.systemd.service_manager",
        "pglift.temboard",
    }


def test_pluginmanager_get(settings: settings.Settings) -> None:
    new_settings = settings.copy(update={"prometheus": None})
    p = pm.PluginManager.get(new_settings)
    assert {name for name, _ in p.list_name_plugin()} == {
        "pglift.databases",
        "pglift.instances",
        "pglift.passfile",
        "pglift.patroni",
        "pglift.pgbackrest",
        "pglift.pgbackrest.repo_path",
        "pglift.postgresql",
        "pglift.powa",
        "pglift.temboard",
    }


def test_pluginmanager_unregister_all(settings: settings.Settings) -> None:
    p = pm.PluginManager.get(settings)
    assert p.list_name_plugin()
    p.unregister_all()
    assert not p.list_name_plugin()


def test_eq(settings: settings.Settings) -> None:
    p1, p2 = pm.PluginManager.get(settings), pm.PluginManager.get(settings)
    assert p1 is not p2
    assert p1 == p2

    p2.unregister_all()
    assert p1 != p2

    assert p1 != object()
    assert 42 != p2
