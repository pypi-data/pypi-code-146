import logging

from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel
from netbox.search import SearchIndex, register_search


class Drive(NetBoxModel):
    size = models.PositiveIntegerField(
        verbose_name="Size (GB)"
    )
    cluster = models.ForeignKey(
        to='virtualization.Cluster',
        on_delete=models.PROTECT,
        related_name='drive',
    )
    virtual_machine = models.ForeignKey(
        to='virtualization.VirtualMachine',
        on_delete=models.CASCADE,
        related_name='drive',
    )
    identifier = models.CharField(
        max_length=255,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = ["size", "cluster", "virtual_machine", "description"]

    prerequisite_models = (
        'virtualization.Cluster',
        'virtualization.VirtualMachine',
    )

    class Meta:
        ordering = ["size"]

    def __str__(self):
        return f"VM: {self.virtual_machine} Size: {self.size} Storage Cluster: {self.cluster}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_disk:drive", kwargs={"pk": self.pk})

    # this is not needed if small_image is created at set_image
    def save(self, *args, **kwargs):
        number_of_hard_drives = Drive.objects.filter(virtual_machine=self.virtual_machine).order_by("created").count()

        logger = logging.getLogger('netbox_disk.Drive')
        logger.info(f"-------- Save Result: {number_of_hard_drives}")

        super(Drive, self).save(*args, **kwargs)


@register_search
class DriveIndex(SearchIndex):
    model = Drive
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
    model = Filesystem
    fields = (
        ("fs", 100)
    )

