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


class DiskTable(DiskBaseTable):
    """Table for displaying Disk objects."""

    pk = ToggleColumn()

    class Meta(NetBoxTable.Meta):
        model = Disk
        fields = (
            "pk",
            "vg_name",
            "lv_name",
            "size",
            "description",
        )
        default_columns = (
            "vg_name",
            "lv_name",
            "size",
        )


class RelatedDiskTable(DiskBaseTable):
    actions = ActionsColumn(actions=())

    class Meta(NetBoxTable.Meta):
        model = Disk
        fields = (
            "vg_name",
            "lv_name",
            "size",
        )
        default_columns = (
            "vg_name",
            "lv_name",
            "size",
        )