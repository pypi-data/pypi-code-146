from django.db import models, transaction
from django.urls import reverse

from netbox.models import NetBoxModel
from netbox.search import SearchIndex, register_search


class Disk(NetBoxModel):
    vg_name = models.CharField(
        unique=False,
        max_length=255,
    )
    lv_name = models.CharField(
        unique=False,
        max_length=255,
    )
    size = models.PositiveIntegerField(
        verbose_name="Size (GB)"
    )
    path = models.CharField(
        unique=False,
        max_length=255,
    )
    cluster = models.ForeignKey(
        to='virtualization.Cluster',
        on_delete=models.PROTECT,
        related_name='disks',
    )
    virtual_machine = models.ForeignKey(
        to='virtualization.VirtualMachine',
        on_delete=models.CASCADE,
        related_name='disks',
    )
    description = models.CharField(
        max_length=200,
        blank=True,
    )

    clone_fields = ["vg_name", "lv_name", "size", "path", "virtual_machine", "description"]

    def get_absolute_url(self):
        return reverse("plugins:netbox_disk:disk", kwargs={"pk": self.id})

    def __str__(self):
        return f"VM: test-vm vg_{self.vg_name}-lv_{self.lv_name}"

    class Meta:
        ordering = ("vg_name", "lv_name", "size", "path")


@register_search
class DiskIndex(SearchIndex):
    model = Disk
    fields = (
        ("vg_name", 100),
        ("lv_name", 150),
        ("size", 200),
        ("path", 200),
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


class Physicalvolume(NetBoxModel):
    size = models.PositiveIntegerField(
        verbose_name="Size (GB)"
    )
    cluster = models.ForeignKey(
        to='virtualization.Cluster',
        on_delete=models.PROTECT,
        related_name='pv',
    )
    virtual_machine = models.ForeignKey(
        to='virtualization.VirtualMachine',
        on_delete=models.CASCADE,
        related_name='pv',
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = ["size", "cluster", "virtual_machine", "description"]

    def get_absolute_url(self):
        return reverse("plugins:netbox_disk:physicalvolume", kwargs={"pk": self.pk})

    def __str__(self):
        return f"PV: {self.virtual_machine}-{self.size}-{self.cluster}"

    class Meta:
        ordering = ["size"]


@register_search
class PhysicalvolumeIndex(SearchIndex):
    model = Physicalvolume
    fields = (
        ("size", 100)
    )
