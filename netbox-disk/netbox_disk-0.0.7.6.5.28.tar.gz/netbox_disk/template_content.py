from django.db.models.functions import Length

from extras.plugins import PluginTemplateExtension

from netbox_disk.models import Disk
from netbox_disk.tables import RelatedDiskTable


class RelatedDisks(PluginTemplateExtension):
    model = "virtualization.virtualmachine"

    def right_page(self):
        obj = self.context.get("object")

        disks = Disk.objects.filter(
            virtual_machine=obj
        )
        disk_table = RelatedDiskTable(
            data=disks
        )

        return self.render(
            "netbox_disk/disk/disk_box.html",
            extra_context={
                "related_disks": disk_table,
            },
        )


template_extensions = [RelatedDisks]
