from extras.plugins import PluginConfig

class NetBoxRisksConfig(PluginConfig):
    name = 'users_and_computers'
    verbose_name = 'Users and Computers'
    description = 'Manage AD Users and Workstations'
    version = '0.0.3'
    base_url = 'users_and_computers'
    author = 'Artur Shamsiev'
    author_email = 'me@z-lab.me'


config = NetBoxRisksConfig
