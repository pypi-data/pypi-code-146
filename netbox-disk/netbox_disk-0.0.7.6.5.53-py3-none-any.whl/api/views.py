from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import APIRootView

from netbox.api.viewsets import NetBoxModelViewSet

from netbox_disk.api.serializers import (
    DriveSerializer,
    FilesystemSerializer,
)
from netbox_disk.filters import DriveFilter, FilesystemFilter
from netbox_disk.models import Drive, Filesystem


class NetboxDiskRootView(APIRootView):
    """
    NetboxDNS API root view
    """

    def get_view_name(self):
        return "NetboxDisk"


class DriveViewSet(NetBoxModelViewSet):
    queryset = Drive.objects.all()
    serializer_class = DriveSerializer
    filterset_class = DriveFilter

    @action(detail=True, methods=["get"])
    def drive(self, request, pk=None):
        drives = Drive.objects.filter(drive__id=pk)
        serializer = DriveSerializer(drives, many=True, context={"request": request})
        return Response(serializer.data)


class FilesystemViewSet(NetBoxModelViewSet):
    queryset = Filesystem.objects.all()
    serializer_class = FilesystemSerializer
    filterset_class = FilesystemFilter

    @action(detail=True, methods=["get"])
    def filesystem(self, request, pk=None):
        filesystem = Filesystem.objects.filter(filesystem__id=pk)
        serializer = FilesystemSerializer(filesystem, many=True, context={"request": request})
        return Response(serializer.data)
