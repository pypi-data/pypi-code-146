import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ChoiceFieldColumn,
    ToggleColumn,
    TagColumn,
    ActionsColumn,
)

from netbox_disk.models import Physicalvolume


class PhysicalvolumeBaseTable(NetBoxTable):
    """Base class for tables displaying PhysicalVolume"""

    size = tables.Column(
        linkify=True,
    )


class PhysicalvolumeTable(PhysicalvolumeBaseTable):
    """Table for displaying PhysicalVolume objects."""

    pk = ToggleColumn()

    class Meta(NetBoxTable.Meta):
        model = Physicalvolume
        fields = (
            "pk",
            "size",
            "description",
        )
        default_columns = (
            "size",
            "description"
        )


class RelatedPhysicalVolumeTable(PhysicalvolumeBaseTable):
    actions = ActionsColumn(actions=())

    class Meta(NetBoxTable.Meta):
        model = Physicalvolume
        fields = (
            "pk",
            "size",
            "description",
        )
        default_columns = (
            "size",
            "description"
        )
