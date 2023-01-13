from netbox.views import generic

from netbox_disk.filters import PhysicalvolumeFilter
from netbox_disk.forms import (
    PhysicalvolumeImportForm,
    PhysicalvolumeFilterForm,
    PhysicalvolumeForm,
    PhysicalvolumeBulkEditForm
)
from netbox_disk.models import Physicalvolume
from netbox_disk.tables import PhysicalvolumeTable


class PhysicalvolumeListView(generic.ObjectListView):
    queryset = Physicalvolume.objects.all()
    filterset = PhysicalvolumeFilter
    filterset_form = PhysicalvolumeFilterForm
    table = PhysicalvolumeTable


class PhysicalvolumeView(generic.ObjectView):
    """Display PhysicalVolume details"""

    queryset = Physicalvolume.objects.all()


class PhysicalvolumeEditView(generic.ObjectEditView):
    """View for editing a PhysicalVolume instance."""

    queryset = Physicalvolume.objects.all()
    form = PhysicalvolumeForm
    default_return_url = "plugins:netbox_disk:physicalvolume_list"


class PhysicalvolumeDeleteView(generic.ObjectDeleteView):
    queryset = Physicalvolume.objects.all()
    default_return_url = "plugins:netbox_disk:physicalvolume_list"


class PhysicalvolumeBulkImportView(generic.BulkImportView):
    queryset = Physicalvolume.objects.all()
    model_form = PhysicalvolumeImportForm
    table = PhysicalvolumeTable
    default_return_url = "plugins:netbox_disk:physicalvolume_list"


class PhysicalvolumeBulkEditView(generic.BulkEditView):
    queryset = Physicalvolume.objects.all()
    filterset = PhysicalvolumeFilter
    table = PhysicalvolumeTable
    form = PhysicalvolumeBulkEditForm


class PhysicalvolumeBulkDeleteView(generic.BulkDeleteView):
    queryset = Physicalvolume.objects.all()
    table = PhysicalvolumeTable
