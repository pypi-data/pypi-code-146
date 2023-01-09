import django_filters
from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet

from netbox_disk.models import Filesystem


class FilesystemFilter(NetBoxModelFilterSet):
    """Filter capabilities for Filesystem instances."""

    class Meta:
        model = Filesystem
        fields = ("filesystem")

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(filesystem__icontains=value)
        )
        return queryset.filter(qs_filter)