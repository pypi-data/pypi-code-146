from netbox.views import generic

from netbox_storage.filters import DriveFilter
from netbox_storage.forms import (
    DriveImportForm,
    DriveFilterForm,
    DriveForm,
    DriveBulkEditForm
)
from netbox_storage.models import Drive
from netbox_storage.tables import DriveTable


class DriveListView(generic.ObjectListView):
    queryset = Drive.objects.all()
    filterset = DriveFilter
    filterset_form = DriveFilterForm
    table = DriveTable


class DriveView(generic.ObjectView):
    """Display Drive details"""

    queryset = Drive.objects.all()


class DriveEditView(generic.ObjectEditView):
    """View for editing a Drive instance."""

    queryset = Drive.objects.all()
    form = DriveForm
    default_return_url = "plugins:netbox_storage:drive_list"


class DriveDeleteView(generic.ObjectDeleteView):
    queryset = Drive.objects.all()
    default_return_url = "plugins:netbox_storage:drive_list"


class DriveBulkImportView(generic.BulkImportView):
    queryset = Drive.objects.all()
    model_form = DriveImportForm
    table = DriveTable
    default_return_url = "plugins:netbox_storage:drive_list"


class DriveBulkEditView(generic.BulkEditView):
    queryset = Drive.objects.all()
    filterset = DriveFilter
    table = DriveTable
    form = DriveBulkEditForm


class DriveBulkDeleteView(generic.BulkDeleteView):
    queryset = Drive.objects.all()
    table = DriveTable
