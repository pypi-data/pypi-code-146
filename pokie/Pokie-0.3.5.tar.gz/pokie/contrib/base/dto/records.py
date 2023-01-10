from rick_db import fieldmapper


@fieldmapper(tablename="settings", pk="id_settings")
class SettingsRecord:
    id = "id_settings"
    module = "module"
    key = "key"
    value = "value"


@fieldmapper(tablename="_fixture", pk="id_fixture")
class FixtureRecord:
    id = "id_fixture"
    applied = "applied"
    name = "name"
