from netbox.views import generic

from netbox_storage.filters import FilesystemFilter
from netbox_storage.forms import (
    FilesystemImportForm,
    FilesystemFilterForm,
    FilesystemForm,
    FilesystemBulkEditForm
)
from netbox_storage.models import Filesystem
from netbox_storage.tables import FilesystemTable


class FilesystemListView(generic.ObjectListView):
    queryset = Filesystem.objects.all()
    filterset = FilesystemFilter
    filterset_form = FilesystemFilterForm
    table = FilesystemTable


class FilesystemView(generic.ObjectView):
    """Display Filesystem details"""

    queryset = Filesystem.objects.all()


class FilesystemEditView(generic.ObjectEditView):
    """View for editing a Filesystem instance."""

    queryset = Filesystem.objects.all()
    form = FilesystemForm
    default_return_url = "plugins:netbox_storage:filesystem_list"


class FilesystemDeleteView(generic.ObjectDeleteView):
    queryset = Filesystem.objects.all()
    default_return_url = "plugins:netbox_storage:filesystem_list"


class FilesystemBulkImportView(generic.BulkImportView):
    queryset = Filesystem.objects.all()
    model_form = FilesystemImportForm
    table = FilesystemTable
    default_return_url = "plugins:netbox_storage:filesystem_list"


class FilesystemBulkEditView(generic.BulkEditView):
    queryset = Filesystem.objects.all()
    filterset = FilesystemFilter
    table = FilesystemTable
    form = FilesystemBulkEditForm


class FilesystemBulkDeleteView(generic.BulkDeleteView):
    queryset = Filesystem.objects.all()
    table = FilesystemTable
