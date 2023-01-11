from django import forms

from django.forms import (
    CharField,
)

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)

from netbox_disk.models import Physicalvolume


class PhysicalvolumeForm(NetBoxModelForm):
    """Form for creating a new PhysicalVolume object."""
    size = CharField(
        required=False,
        label="Size (GB)",
    )

    class Meta:
        model = Physicalvolume

        fields = (
            "size",
            "description",
        )


class PhysicalvolumeFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering PhysicalVolume instances."""

    model = Physicalvolume

    size = CharField(
        required=False,
        label="Size (GB)",
    )


class PhysicalvolumeImportForm(NetBoxModelImportForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Physicalvolume

        fields = (
            "size",
            "description",
        )


class PhysicalvolumeBulkEditForm(NetBoxModelBulkEditForm):
    model = Physicalvolume

    size = CharField(
        required=False,
        label="Size (GB)",
    )
    description = CharField(max_length=255, required=False)

    fieldsets = (
        (
            None,
            ("size", "description"),
        ),
    )
    nullable_fields = ["description"]
