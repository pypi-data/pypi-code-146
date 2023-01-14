from extras.plugins import PluginConfig
from .version import __version__


class UsersandcomputersConfig(PluginConfig):
    name = 'users_and_computers'
    verbose_name = 'Users and Computers'
    description = 'Manage AD Users and Workstations'
    version = __version__
    author = 'Artur Shamsiev'
    author_email = 'me@z-lab.me'
    required_settings = []
    default_settings = {}


config = UsersandcomputersConfig # noqa
