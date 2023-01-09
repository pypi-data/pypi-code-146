from netbox.api.routers import NetBoxRouter

from netbox_disk.api.views import (
    NetboxDiskRootView,
    DiskViewSet
)

router = NetBoxRouter()
router.APIRootView = NetboxDiskRootView

router.register("disks", DiskViewSet)

urlpatterns = router.urls