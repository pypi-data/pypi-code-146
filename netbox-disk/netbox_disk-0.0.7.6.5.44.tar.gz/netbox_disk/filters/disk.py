import django_filters
from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet

from netbox_disk.models import Disk
from virtualization.models import Cluster, VirtualMachine


class DiskFilter(NetBoxModelFilterSet):
    """Filter capabilities for Disk instances."""
    cluster = django_filters.ModelMultipleChoiceFilter(
        field_name='cluster__name',
        queryset=Cluster.objects.all(),
        to_field_name='name',
        label='Cluster',
    )
    virtual_machine = django_filters.ModelMultipleChoiceFilter(
        field_name='virtual_machine__name',
        queryset=VirtualMachine.objects.all(),
        to_field_name='name',
        label='Virtual machine (name)',
    )

    class Meta:
        model = Disk
        fields = ("vg_name", "lv_name", "size", "path", "cluster", "virtual_machine")

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
