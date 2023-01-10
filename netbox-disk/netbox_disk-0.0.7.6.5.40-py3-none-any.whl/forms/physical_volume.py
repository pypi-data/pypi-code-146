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

from netbox_disk.models import PhysicalVolume


class PhysicalVolumeForm(NetBoxModelForm):
    """Form for creating a new PhysicalVolume object."""
    size = CharField(
        required=False,
        label="Size (GB)",
    )

    class Meta:
        model = PhysicalVolume

        fields = (
            "size",
            "description",
        )


class PhysicalVolumeFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering PhysicalVolume instances."""

    model = PhysicalVolume

    size = CharField(
        required=False,
        label="Size (GB)",
    )


class PhysicalVolumeImportForm(NetBoxModelImportForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = PhysicalVolume

        fields = (
            "size",
            "description",
        )


class PhysicalVolumeBulkEditForm(NetBoxModelBulkEditForm):
    model = PhysicalVolume

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
