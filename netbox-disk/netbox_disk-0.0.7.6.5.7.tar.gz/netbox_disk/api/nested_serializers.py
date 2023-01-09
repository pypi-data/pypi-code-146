from rest_framework import serializers

from netbox.api.serializers import WritableNestedSerializer

from netbox_disk.models import Disk


#
# Disks
#
class NestedDiskSerializer(WritableNestedSerializer):
    class Meta:
        model = Disk
        fields = [
            "id",
            "vg_name",
            "lv_name",
            "size",
        ]
