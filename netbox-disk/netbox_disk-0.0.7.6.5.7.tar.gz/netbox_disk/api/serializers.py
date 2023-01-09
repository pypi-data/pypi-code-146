from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer

from netbox_disk.api.nested_serializers import (
    NestedDiskSerializer
)
from netbox_disk.models import Disk


class DiskSerializer(NetBoxModelSerializer):

    class Meta:
        model = Disk
        fields = (
            "id",
            "vg_name",
            "lv_name",
            "size",
            "description",
            "created",
            "last_updated",
            #            "custom_fields",
        )
