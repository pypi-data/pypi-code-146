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
from virtualization.models import Cluster, VirtualMachine


class DiskForm(NetBoxModelForm):
    """Form for creating a new Disk object."""
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        query_params={
            'site_id': '$site',
            'group_id': '$cluster_group',
        }
    )
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False
    )

    class Meta:
        model = Disk

        fields = (
            "vg_name",
            "lv_name",
            "size",
            "path",
            "cluster",
            "virtual_machine",
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
    path = CharField(
        required=False,
        label="Path",
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        query_params={
            'site_id': '$site',
            'group_id': '$cluster_group',
        }
    )
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False
    )


class DiskImportForm(NetBoxModelImportForm):
    cluster = CSVModelChoiceField(
        queryset=Cluster.objects.all(),
        to_field_name='name',
        required=False,
        help_text='Assigned cluster'
    )
    virtual_machine = CSVModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        to_field_name='name',
        help_text='Required'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Disk

        fields = (
            "vg_name",
            "lv_name",
            "size",
            "path",
            "cluster",
            "virtual_machine",
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
    path = CharField(
        required=False,
        label="Path",
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        query_params={
            'site_id': '$site'
        }
    )
    virtual_machine = CSVModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        to_field_name='name',
        help_text='Required'
    )
    description = CharField(max_length=200, required=False)

    fieldsets = (
        (
            None,
            ("vg_name", "lv_name", "size", "path", "cluster", "virtual_machine", "description"),
        ),
    )
    nullable_fields = ("description")
