from rest_framework import serializers

from netbox_disk.models import Disk, Filesystem, Physicalvolume
from virtualization.api.nested_serializers import NestedClusterSerializer, NestedVirtualMachineSerializer


class DiskSerializer(serializers.ModelSerializer):
    cluster = NestedClusterSerializer(required=False, allow_null=True)
    virtual_machine = NestedVirtualMachineSerializer(required=False, allow_null=True)

    class Meta:
        model = Disk
        fields = (
            "id",
            "vg_name",
            "lv_name",
            "size",
            "path",
            "description",
            "cluster",
            "virtual_machine",
            "created",
            "last_updated",
            "custom_fields",
        )


class FilesystemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Filesystem
        fields = (
            "id",
            "fs",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class PhysicalvolumeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Physicalvolume
        fields = (
            "id",
            "size",
            "cluster",
            "virtual_machine",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )
