from cliff.command import Command

from enough import settings
from enough.common import options
from enough.common.openstack import OpenStack


class Cli(Command):
    "OpenStack client"

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('args', nargs='+')
        return options.set_options(parser)

    def take_action(self, parsed_args):
        args = vars(self.app.options)
        args.update(vars(parsed_args))
        o = OpenStack(settings.CONFIG_DIR, **args)
        o.run(args['args'])
