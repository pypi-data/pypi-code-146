import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
    ActionsColumn,
)

from netbox_storage.models import Drive


class DriveBaseTable(NetBoxTable):
    """Base class for tables displaying Drives"""

    identifier = tables.Column(
        linkify=True
    )
    size = tables.Column(
        linkify=True
    )
    cluster = tables.Column(
        linkify=True
    )


class DriveTable(DriveBaseTable):
    """Table for displaying Drives objects."""

    pk = ToggleColumn()
    virtual_machine = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = Drive
        fields = (
            "pk",
            "size",
            "cluster",
            "identifier",
            "virtual_machine",
            "description",
        )
        default_columns = (
            "virtual_machine",
            "identifier",
            "size",
            "cluster",
        )


class RelatedDriveTable(DriveBaseTable):
    actions = ActionsColumn(actions=())

    class Meta(NetBoxTable.Meta):
        model = Drive
        fields = (
            "size",
            "cluster",
        )
        default_columns = (
            "size",
            "cluster",
            "identifier",
        )
