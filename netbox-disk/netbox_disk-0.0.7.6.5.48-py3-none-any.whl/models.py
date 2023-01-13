from django.db import models, transaction
from django.urls import reverse

from netbox.models import NetBoxModel
from netbox.search import SearchIndex, register_search


class Disk(NetBoxModel):
    size = models.PositiveIntegerField(
        verbose_name="Size (GB)"
    )
    cluster = models.ForeignKey(
        to='virtualization.Cluster',
        on_delete=models.PROTECT,
        related_name='disk',
    )
    virtual_machine = models.ForeignKey(
        to='virtualization.VirtualMachine',
        on_delete=models.CASCADE,
        related_name='disk',
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = ["size", "virtual_machine", "description"]

    def get_absolute_url(self):
        return reverse("plugins:netbox_disk:disk", kwargs={"pk": self.id})

    def __str__(self):
        return f"VM: test-vm vg_{self.size}-lv_{self.size}"

    class Meta:
        ordering = ("size")


@register_search
class DiskIndex(SearchIndex):
    model = Disk
    fields = (
        ("size", 200),
    )


class Filesystem(NetBoxModel):
    fs = models.CharField(
        unique=True,
        max_length=255,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = ["fs", "description"]

    def get_absolute_url(self):
        return reverse("plugins:netbox_disk:filesystem", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.fs}"

    class Meta:
        ordering = ("fs", "description")


@register_search
class FilesystemIndex(SearchIndex):
    model = Disk
    fields = (
        ("fs", 100)
    )

