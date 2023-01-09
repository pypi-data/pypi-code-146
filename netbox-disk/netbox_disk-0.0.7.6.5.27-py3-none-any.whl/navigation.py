from extras.plugins import PluginMenuButton, PluginMenuItem
from extras.plugins import PluginMenu
from utilities.choices import ButtonColorChoices

disk_menu_item = PluginMenuItem(
    link="plugins:netbox_disk:disk_list",
    link_text="Disks",
    permissions=["netbox_disk.disk_view"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_disk:disk_add",
            "Add",
            "mdi mdi-plus-thick",
            ButtonColorChoices.GREEN,
            permissions=["netbox_disk.add_disk"],
        ),
        PluginMenuButton(
            "plugins:netbox_disk:disk_import",
            "Import",
            "mdi mdi-upload",
            ButtonColorChoices.CYAN,
            permissions=["netbox_disk.add_disk"],
        ),
    ),
)


menu = PluginMenu(
    label="NetBox Disk",
    groups=(
        (
            "Disk Configuration",
            (
                disk_menu_item,
            ),
        ),
    ),
    icon_class="mdi mdi-disc",
)