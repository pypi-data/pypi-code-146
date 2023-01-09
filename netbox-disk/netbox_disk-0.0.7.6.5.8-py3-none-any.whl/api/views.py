from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import APIRootView

from netbox.api.viewsets import NetBoxModelViewSet

from netbox_disk.api.serializers import (
    DiskSerializer
)
from netbox_disk.filters import DiskFilter
from netbox_disk.models import Disk


class NetboxDiskRootView(APIRootView):
    """
    NetboxDNS API root view
    """

    def get_view_name(self):
        return "NetboxDisk"


class DiskViewSet(NetBoxModelViewSet):
    queryset = Disk.objects.all()
    serializer_class = DiskSerializer
    filterset_class = DiskFilter

    @action(detail=True, methods=["get"])
    def disks(self, request, pk=None):
        disks = Disk.objects.filter(disks__id=pk)
        serializer = DiskSerializer(disks, many=True, context={"request": request})
        return Response(serializer.data)
