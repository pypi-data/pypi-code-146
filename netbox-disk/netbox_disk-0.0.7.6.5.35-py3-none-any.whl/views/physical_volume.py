from netbox.views import generic

from netbox_disk.filters import PhysicalVolumeFilter
from netbox_disk.forms import (
    PhysicalVolumeImportForm,
    PhysicalVolumeFilterForm,
    PhysicalVolumeForm,
    PhysicalVolumeBulkEditForm
)
from netbox_disk.models import PhysicalVolume
from netbox_disk.tables import PhysicalVolumeTable


class PhysicalVolumeListView(generic.ObjectListView):
    queryset = PhysicalVolume.objects.all()
    filterset = PhysicalVolumeFilter
    filterset_form = PhysicalVolumeFilterForm
    table = PhysicalVolumeTable


class PhysicalVolumeView(generic.ObjectView):
    """Display PhysicalVolume details"""

    queryset = PhysicalVolume.objects.all()


class PhysicalVolumeEditView(generic.ObjectEditView):
    """View for editing a PhysicalVolume instance."""

    queryset = PhysicalVolume.objects.all()
    form = PhysicalVolumeForm
    default_return_url = "plugins:netbox_disk:physical_volume_list"


class PhysicalVolumeDeleteView(generic.ObjectDeleteView):
    queryset = PhysicalVolume.objects.all()
    default_return_url = "plugins:netbox_disk:physical_volume_list"


class PhysicalVolumeBulkImportView(generic.BulkImportView):
    queryset = PhysicalVolume.objects.all()
    model_form = PhysicalVolumeImportForm
    table = PhysicalVolumeTable
    default_return_url = "plugins:netbox_disk:physical_volume_list"


class PhysicalVolumeBulkEditView(generic.BulkEditView):
    queryset = PhysicalVolume.objects.all()
    filterset = PhysicalVolumeFilter
    table = PhysicalVolumeTable
    form = PhysicalVolumeBulkEditForm


class PhysicalVolumeBulkDeleteView(generic.BulkDeleteView):
    queryset = PhysicalVolume.objects.all()
    table = PhysicalVolumeTable
