from extras.plugins import PluginConfig

__version__ = "0.0.7.6.5.62"


class DiskConfig(PluginConfig):
    name = "netbox_disk"
    verbose_name = "Netbox Storage"
    description = "Netbox Storage"
    min_version = "3.4.0"
    version = __version__
    author = "Tim Rhomberg"
    author_email = "timrhomberg@hotmail.cm.com"
    required_settings = []
    base_url = "netbox-disk"


config = DiskConfig
