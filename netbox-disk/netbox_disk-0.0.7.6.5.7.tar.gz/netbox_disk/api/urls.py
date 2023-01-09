from netbox.api.routers import NetBoxRouter

from netbox_dns.api.views import (
    NetboxDNSRootView,
    ViewViewSet,
    ZoneViewSet,
    NameServerViewSet,
    RecordViewSet,
    DiskViewSet
)

router = NetBoxRouter()
router.APIRootView = NetboxDiskRootView

router.register("views", ViewViewSet)
router.register("zones", ZoneViewSet)
router.register("nameservers", NameServerViewSet)
router.register("disks", DiskViewSet)

urlpatterns = router.urls