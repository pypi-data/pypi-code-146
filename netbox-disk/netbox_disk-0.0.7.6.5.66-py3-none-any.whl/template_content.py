from extras.plugins import PluginTemplateExtension

from netbox_storage.models import Drive
from netbox_storage.tables import RelatedDriveTable


class RelatedDrives(PluginTemplateExtension):
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
            "netbox_storage/storage/storage_box.html",
            extra_context={
                "related_drives": drive_table,
            },
        )


template_extensions = [RelatedDrives]
