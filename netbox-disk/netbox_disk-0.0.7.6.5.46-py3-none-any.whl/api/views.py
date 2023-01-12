from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import APIRootView

from netbox.api.viewsets import NetBoxModelViewSet

from netbox_disk.api.serializers import (
    DiskSerializer,
    FilesystemSerializer,
    PhysicalvolumeSerializer
)
from netbox_disk.filters import DiskFilter, FilesystemFilter, PhysicalvolumeFilter
from netbox_disk.models import Disk, Filesystem, Physicalvolume


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


class FilesystemViewSet(NetBoxModelViewSet):
    queryset = Filesystem.objects.all()
    serializer_class = FilesystemSerializer
    filterset_class = FilesystemFilter

    @action(detail=True, methods=["get"])
    def filesystem(self, request, pk=None):
        filesystem = Filesystem.objects.filter(filesystem__id=pk)
        serializer = FilesystemSerializer(filesystem, many=True, context={"request": request})
        return Response(serializer.data)


class PhysicalvolumeViewSet(NetBoxModelViewSet):
    queryset = Physicalvolume.objects.all()
    serializer_class = PhysicalvolumeSerializer
    filterset_class = PhysicalvolumeFilter

    @action(detail=True, methods=["get"])
    def physicalvolume(self, request, pk=None):
        physicalvolume = Physicalvolume.objects.filter(physicalvolume__id=pk)
        serializer = PhysicalvolumeSerializer(physicalvolume, many=True, context={"request": request})
        return Response(serializer.data)
