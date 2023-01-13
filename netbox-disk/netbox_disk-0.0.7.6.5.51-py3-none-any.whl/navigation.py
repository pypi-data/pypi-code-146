from extras.plugins import PluginMenuButton, PluginMenuItem
from extras.plugins import PluginMenu
from utilities.choices import ButtonColorChoices

drive_menu_item = PluginMenuItem(
    link="plugins:netbox_disk:drive_list",
    link_text="Drives",
    permissions=["netbox_disk.drive_view"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_disk:drive_add",
            "Add",
            "mdi mdi-plus-thick",
            ButtonColorChoices.GREEN,
            permissions=["netbox_disk.add_drive"],
        ),
        PluginMenuButton(
            "plugins:netbox_disk:drive_import",
            "Import",
            "mdi mdi-upload",
            ButtonColorChoices.CYAN,
            permissions=["netbox_disk.add_drive"],
        ),
    ),
)

filesystem_menu_item = PluginMenuItem(
    link="plugins:netbox_disk:filesystem_list",
    link_text="Filesystem",
    permissions=["netbox_disk.disk_view"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_disk:filesystem_add",
            "Add",
            "mdi mdi-plus-thick",
            ButtonColorChoices.GREEN,
            permissions=["netbox_disk.add_disk"],
        ),
        PluginMenuButton(
            "plugins:netbox_disk:filesystem_import",
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
                drive_menu_item,
                filesystem_menu_item,
            ),
        ),
    ),
    icon_class="mdi mdi-disc",
)
