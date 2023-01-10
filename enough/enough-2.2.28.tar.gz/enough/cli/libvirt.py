from cliff.command import Command

from enough import settings
from enough.common import Enough


class Install(Command):
    "Install"

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--vpn', help='relative path to VPN credentials')
        parser.add_argument('host')
        return parser

    def take_action(self, parsed_args):
        args = vars(self.app.options)
        args.update(vars(parsed_args))
        args['driver'] = 'libvirt'
        e = Enough(settings.CONFIG_DIR, settings.SHARE_DIR, **args)
        e.libvirt_install()


class Network(Command):
    "Network"

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        args = vars(self.app.options)
        args.update(vars(parsed_args))
        args['driver'] = 'libvirt'
        e = Enough(settings.CONFIG_DIR, settings.SHARE_DIR, **args)
        e.libvirt.networks_create()
