from rest_framework import serializers

from netbox_disk.models import Drive, Filesystem
from virtualization.api.nested_serializers import NestedClusterSerializer, NestedVirtualMachineSerializer


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


class DriveSerializer(serializers.ModelSerializer):
    cluster = NestedClusterSerializer(required=False, allow_null=True)
    virtual_machine = NestedVirtualMachineSerializer(required=False, allow_null=True)

    class Meta:
        model = Drive
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
