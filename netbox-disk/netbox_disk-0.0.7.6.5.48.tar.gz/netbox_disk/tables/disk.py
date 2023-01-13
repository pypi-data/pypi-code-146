import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ChoiceFieldColumn,
    ToggleColumn,
    TagColumn,
    ActionsColumn,
)

from netbox_disk.models import Disk


class DiskBaseTable(NetBoxTable):
    """Base class for tables displaying Disks"""

    size = tables.Column()
    cluster = tables.Column(
        linkify=True
    )


class DiskTable(DiskBaseTable):
    """Table for displaying Disk objects."""

    pk = ToggleColumn()
    virtual_machine = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = Disk
        fields = (
            "pk",
            "size",
            "cluster",
            "virtual_machine",
            "description",
        )
        default_columns = (
            "virtual_machine",
            "size",
            "cluster",
        )


class RelatedDiskTable(DiskBaseTable):
    actions = ActionsColumn(actions=())

    class Meta(NetBoxTable.Meta):
        model = Disk
        fields = (
            "size",
            "cluster",
        )
        default_columns = (
            "size",
            "cluster",
        )
