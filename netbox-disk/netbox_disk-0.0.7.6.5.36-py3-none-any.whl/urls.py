from django.urls import path

from netbox.views.generic import ObjectChangeLogView

from netbox_disk.models import Disk, Filesystem, PhysicalVolume
from netbox_disk.views import (
    # disk
    DiskListView,
    DiskView,
    DiskEditView,
    DiskDeleteView,
    DiskBulkImportView,
    DiskBulkEditView,
    DiskBulkDeleteView,
    # filesystem
    FilesystemListView,
    FilesystemView,
    FilesystemEditView,
    FilesystemDeleteView,
    FilesystemBulkImportView,
    FilesystemBulkEditView,
    FilesystemBulkDeleteView,
    # physical volume
    PhysicalVolumeListView,
    PhysicalVolumeView,
    PhysicalVolumeEditView,
    PhysicalVolumeDeleteView,
    PhysicalVolumeBulkImportView,
    PhysicalVolumeBulkEditView,
    PhysicalVolumeBulkDeleteView,
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
    #
    # Filesystem urls
    #
    path("filesystem/", FilesystemListView.as_view(), name="filesystem_list"),
    path("filesystem/add/", FilesystemEditView.as_view(), name="filesystem_add"),
    path("filesystem/import/", FilesystemBulkImportView.as_view(), name="filesystem_import"),
    path("filesystem/edit/", FilesystemBulkEditView.as_view(), name="filesystem_bulk_edit"),
    path("filesystem/delete/", FilesystemBulkDeleteView.as_view(), name="filesystem_bulk_delete"),
    path("filesystem/<int:pk>/", FilesystemView.as_view(), name="filesystem"),
    path("filesystem/<int:pk>/edit/", FilesystemEditView.as_view(), name="filesystem_edit"),
    path("filesystem/<int:pk>/delete/", FilesystemDeleteView.as_view(), name="filesystem_delete"),
    path(
        "filesystem/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="filesystem_changelog",
        kwargs={"model": Filesystem},
    ),
    #
    # physical_volume
    #
    path("physical_volume/", PhysicalVolumeListView.as_view(), name="filesystem_list"),
    path("physical_volume/add/", PhysicalVolumeEditView.as_view(), name="filesystem_add"),
    path("physical_volume/import/", PhysicalVolumeBulkImportView.as_view(), name="filesystem_import"),
    path("physical_volume/edit/", PhysicalVolumeBulkEditView.as_view(), name="filesystem_bulk_edit"),
    path("physical_volume/delete/", PhysicalVolumeBulkDeleteView.as_view(), name="filesystem_bulk_delete"),
    path("physical_volume/<int:pk>/", PhysicalVolumeView.as_view(), name="filesystem"),
    path("physical_volume/<int:pk>/edit/", PhysicalVolumeEditView.as_view(), name="filesystem_edit"),
    path("physical_volume/<int:pk>/delete/", PhysicalVolumeDeleteView.as_view(), name="filesystem_delete"),
    path(
        "physical_volume/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="physical_volume_changelog",
        kwargs={"model": PhysicalVolume},
    ),
]
