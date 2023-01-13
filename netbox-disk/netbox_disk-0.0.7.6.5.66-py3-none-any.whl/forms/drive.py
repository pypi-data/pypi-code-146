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
    CSVModelChoiceField,
    DynamicModelChoiceField,
)

from netbox_storage.models import Drive
from virtualization.models import Cluster, VirtualMachine


class DriveForm(NetBoxModelForm):
    """Form for creating a new Drive object."""
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
        model = Drive

        fields = (
            "size",
            "cluster",
            "virtual_machine",
            "description",
        )


class DriveFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering Drive instances."""

    model = Drive

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


class DriveImportForm(NetBoxModelImportForm):
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
        model = Drive

        fields = (
            "size",
            "cluster",
            "virtual_machine",
            "description",
        )


class DriveBulkEditForm(NetBoxModelBulkEditForm):
    model = Drive

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
