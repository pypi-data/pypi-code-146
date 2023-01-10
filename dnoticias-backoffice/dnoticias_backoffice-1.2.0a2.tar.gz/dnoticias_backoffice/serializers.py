from django.contrib.auth.models import Permission

from rest_framework import serializers


class PermissionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = (
            "pk",
            "name"
        )

    def get_name(self, obj):
        return obj.__str__()
