from extras.plugins import PluginConfig
from .version import __version__

class NetBoxRisksConfig(PluginConfig):
    name = 'users_and_computers'
    verbose_name = 'Users and Computers'
    description = 'Manage AD Users and Workstations'
    version = __version__
    base_url = 'users_and_computers'
    author = 'Artur Shamsiev'
    author_email = 'me@z-lab.me'

config = NetBoxRisksConfig
