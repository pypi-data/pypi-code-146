from extras.plugins import PluginTemplateExtension

from netbox_disk.models import Drive
from netbox_disk.tables import RelatedDriveTable


class RelatedDisks(PluginTemplateExtension):
    model = "virtualization.virtualmachine"

    def right_page(self):
        obj = self.context.get("object")

        drives = Drive.objects.filter(
            virtual_machine=obj
        )
        drive_table = RelatedDriveTable(
            data=drives
        )

        return self.render(
            "netbox_disk/disk/disk_box.html",
            extra_context={
                "related_drives": drive_table,
            },
        )


template_extensions = [RelatedDisks]
