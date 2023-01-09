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

    vg_name = tables.Column(
        linkify=True,
    )
    lv_name = tables.Column()
    size = tables.Column()
    path = tables.Column()
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
            "vg_name",
            "lv_name",
            "size",
            "path",
            "cluster",
            "virtual_machine",
            "description",
        )
        default_columns = (
            "virtual_machine",
            "vg_name",
            "lv_name",
            "size",
            "path",
            "cluster",
        )


class RelatedDiskTable(DiskBaseTable):
    actions = ActionsColumn(actions=())

    class Meta(NetBoxTable.Meta):
        model = Disk
        fields = (
            "vg_name",
            "lv_name",
            "size",
            "path",
            "cluster",
        )
        default_columns = (
            "vg_name",
            "lv_name",
            "size",
            "path",
            "cluster",
        )
