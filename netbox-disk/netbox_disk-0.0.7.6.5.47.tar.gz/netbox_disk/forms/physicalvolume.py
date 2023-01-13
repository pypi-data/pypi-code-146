from django import forms

from django.forms import (
    CharField,
    IntegerField,
)

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

from netbox_disk.models import Physicalvolume
from virtualization.models import Cluster, VirtualMachine


class PhysicalvolumeForm(NetBoxModelForm):
    """Form for creating a new PhysicalVolume object."""
    size = IntegerField(
        required=False,
        label="Size (GB)",
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

    class Meta:
        model = Physicalvolume

        fields = (
            "size",
            "cluster",
            "virtual_machine",
            "description",
        )


class PhysicalvolumeFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering PhysicalVolume instances."""

    model = Physicalvolume

    size = IntegerField(
        required=False,
        label="Size (GB)",
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


class PhysicalvolumeImportForm(NetBoxModelImportForm):
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
        model = Physicalvolume

        fields = (
            "size",
            "cluster",
            "virtual_machine",
            "description",
        )


class PhysicalvolumeBulkEditForm(NetBoxModelBulkEditForm):
    model = Physicalvolume

    size = IntegerField(
        required=False,
        label="Size (GB)",
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
    description = CharField(max_length=255, required=False)

    fieldsets = (
        (
            None,
            ("size", "cluster", "virtual_machine", "description"),
        ),
    )
    nullable_fields = ["description"]
