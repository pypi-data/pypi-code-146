from netbox.api.routers import NetBoxRouter

from netbox_disk.api.views import (
    NetboxDiskRootView,
    DriveViewSet,
    FilesystemViewSet,
)

router = NetBoxRouter()
router.APIRootView = NetboxDiskRootView

router.register("disk", DriveViewSet)
router.register("filesystem", FilesystemViewSet)

urlpatterns = router.urls
