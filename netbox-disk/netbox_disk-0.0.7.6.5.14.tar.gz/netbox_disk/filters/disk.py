import django_filters
from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet

from netbox_disk.models import Disk


class DiskFilter(NetBoxModelFilterSet):
    """Filter capabilities for Disk instances."""
    managed = django_filters.BooleanFilter()

    class Meta:
        model = Disk
        fields = ("vg_name", "lv_name", "size", "path", "managed")

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(vg_name__icontains=value)
            | Q(lv_name__icontains=value)
            | Q(size__icontains=value)
        )
        return queryset.filter(qs_filter)