from django import forms

from django.forms import (
    CharField,
    IntegerField,
    BooleanField,
    NullBooleanField,
)
from django.urls import reverse_lazy

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)
from utilities.forms import (
    add_blank_choice,
    BulkEditNullBooleanSelect,
    DynamicModelMultipleChoiceField,
    TagFilterField,
    StaticSelect,
    CSVChoiceField,
    CSVModelChoiceField,
    DynamicModelChoiceField,
    APISelect,
    StaticSelectMultiple,
    add_blank_choice,
)

from netbox_disk.models import Disk


class DiskForm(NetBoxModelForm):
    """Form for creating a new Disk object."""

    class Meta:
        model = Disk

        fields = (
            "vg_name",
            "lv_name",
            "size",
            "description",
        )


class DiskFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering Disk instances."""

    model = Disk

    vg_name = CharField(
        required=False,
        label="VG Name",
    )
    lv_name = CharField(
        required=False,
        label="LV Name",
    )
    size = IntegerField(
        required=False,
        label="Size (GB)",
    )


class DiskImportForm(NetBoxModelImportForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Disk

        fields = (
            "vg_name",
            "lv_name",
            "size",
            "description",
        )


class DiskBulkEditForm(NetBoxModelBulkEditForm):
    model = Disk

    vg_name = CharField(
        required=False,
        label="VG Name",
    )
    lv_name = CharField(
        required=False,
        label="LV Name",
    )
    size = IntegerField(
        required=False,
        label="Size (GB)",
    )
    description = CharField(max_length=200, required=False)

    fieldsets = (
        (
            None,
            ("vg_name", "lv_name", "size", "description"),
        ),
    )
    nullable_fields = ("description")