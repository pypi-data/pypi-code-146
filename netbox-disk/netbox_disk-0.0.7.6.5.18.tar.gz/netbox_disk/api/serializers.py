from rest_framework import serializers

from netbox_disk.models import Disk
from virtualization.api.nested_serializers import NestedClusterSerializer


class DiskSerializer(serializers.ModelSerializer):
    cluster = NestedClusterSerializer(required=False, allow_null=True)

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
            "created",
            "last_updated",
            "custom_fields",
        )
