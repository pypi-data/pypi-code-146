from netbox.api.routers import NetBoxRouter

from netbox_disk.api.views import (
    NetboxDiskRootView,
    DiskViewSet,
    FilesystemViewSet
)

router = NetBoxRouter()
router.APIRootView = NetboxDiskRootView

router.register("disks", DiskViewSet)
router.register("filesystem", FilesystemViewSet)

urlpatterns = router.urls
