import django_filters
from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet

from netbox_disk.models import Physicalvolume


class PhysicalvolumeFilter(NetBoxModelFilterSet):
    """Filter capabilities for Filesystem instances."""

    class Meta:
        model = Physicalvolume
        fields = ["size"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(size__icontains=value)
        )
        return queryset.filter(qs_filter)
