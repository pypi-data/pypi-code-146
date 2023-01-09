from rest_framework import serializers

from netbox_disk.models import Disk


class DiskSerializer(serializers.ModelSerializer):

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
            "custom_fields",
        )
