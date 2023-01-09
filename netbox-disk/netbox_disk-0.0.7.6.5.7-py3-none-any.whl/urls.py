from django.urls import path

from netbox.views.generic import ObjectChangeLogView

from netbox_disk.models import Disk
from netbox_disk.views import (
    # disk
    DiskListView,
    DiskView,
    DiskEditView,
    DiskDeleteView,
    DiskBulkImportView,
    DiskBulkEditView,
    DiskBulkDeleteView,
)

app_name = "netbox_disk"

urlpatterns = [
    #
    # Disk urls
    #
    path("disks/", DiskListView.as_view(), name="disk_list"),
    path("disks/add/", DiskEditView.as_view(), name="disk_add"),
    path("disks/import/", DiskBulkImportView.as_view(), name="disk_import"),
    path("disks/edit/", DiskBulkEditView.as_view(), name="disk_bulk_edit"),
    path("disks/delete/", DiskBulkDeleteView.as_view(), name="disk_bulk_delete"),
    path("disks/<int:pk>/", DiskView.as_view(), name="disk"),
    path("disks/<int:pk>/edit/", DiskEditView.as_view(), name="disk_edit"),
    path("disks/<int:pk>/delete/", DiskDeleteView.as_view(), name="disk_delete"),
    path(
        "disks/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="disk_changelog",
        kwargs={"model": Disk},
    ),
]