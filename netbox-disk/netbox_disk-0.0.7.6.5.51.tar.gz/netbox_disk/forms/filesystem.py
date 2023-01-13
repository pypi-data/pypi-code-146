
from django.forms import (
    CharField,

)

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)


from netbox_disk.models import Filesystem


class FilesystemForm(NetBoxModelForm):
    """Form for creating a new Filesystem object."""
    fs = CharField(
        required=False,
        label="Filesystem Name",
    )

    class Meta:
        model = Filesystem

        fields = (
            "fs",
            "description",
        )


class FilesystemFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering Filesystem instances."""

    model = Filesystem

    fs = CharField(
        required=False,
        label="Name",
    )


class FilesystemImportForm(NetBoxModelImportForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Filesystem

        fields = (
            "fs",
            "description",
        )


class FilesystemBulkEditForm(NetBoxModelBulkEditForm):
    model = Filesystem

    fs = CharField(
        required=False,
        label="Name",
    )
    description = CharField(max_length=255, required=False)

    fieldsets = (
        (
            None,
            ("fs", "description"),
        ),
    )
    nullable_fields = ["description"]
