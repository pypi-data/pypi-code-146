from django.urls import path

from netbox.views.generic import ObjectChangeLogView

from netbox_storage.models import Drive, Filesystem
from netbox_storage.views import (
    # Drive View
    DriveListView,
    DriveView,
    DriveEditView,
    DriveDeleteView,
    DriveBulkImportView,
    DriveBulkEditView,
    DriveBulkDeleteView,
    # Filesystem Views
    FilesystemListView,
    FilesystemView,
    FilesystemEditView,
    FilesystemDeleteView,
    FilesystemBulkImportView,
    FilesystemBulkEditView,
    FilesystemBulkDeleteView,
)

app_name = "netbox_storage"

urlpatterns = [
    #
    # Drive urls
    #
    path("drive/", DriveListView.as_view(), name="drive_list"),
    path("drive/add/", DriveEditView.as_view(), name="drive_add"),
    path("drive/import/", DriveBulkImportView.as_view(), name="drive_import"),
    path("drive/edit/", DriveBulkEditView.as_view(), name="drive_bulk_edit"),
    path("drive/delete/", DriveBulkDeleteView.as_view(), name="drive_bulk_delete"),
    path("drive/<int:pk>/", DriveView.as_view(), name="drive"),
    path("drive/<int:pk>/edit/", DriveEditView.as_view(), name="drive_edit"),
    path("drive/<int:pk>/delete/", DriveDeleteView.as_view(), name="drive_delete"),
    path(
        "drive/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="drive_changelog",
        kwargs={"model": Drive},
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
]
