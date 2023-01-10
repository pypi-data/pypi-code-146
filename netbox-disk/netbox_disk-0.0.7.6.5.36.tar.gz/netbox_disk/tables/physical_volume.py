import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ChoiceFieldColumn,
    ToggleColumn,
    TagColumn,
    ActionsColumn,
)

from netbox_disk.models import PhysicalVolume


class PhysicalVolumeBaseTable(NetBoxTable):
    """Base class for tables displaying PhysicalVolume"""

    size = tables.Column(
        linkify=True,
    )


class PhysicalVolumeTable(PhysicalVolumeBaseTable):
    """Table for displaying PhysicalVolume objects."""

    pk = ToggleColumn()

    class Meta(NetBoxTable.Meta):
        model = PhysicalVolume
        fields = (
            "pk",
            "size",
            "description",
        )
        default_columns = (
            "fs",
            "description"
        )


class RelatedPhysicalVolumeTable(PhysicalVolumeBaseTable):
    actions = ActionsColumn(actions=())

    class Meta(NetBoxTable.Meta):
        model = PhysicalVolume
        fields = (
            "pk",
            "size",
            "description",
        )
        default_columns = (
            "size",
            "description"
        )
