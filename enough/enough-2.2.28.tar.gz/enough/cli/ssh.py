from cliff.command import Command

from enough import settings
from enough.common import options
from enough.common import ssh


class SSH(Command):
    "SSH to host"

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('host')
        parser.add_argument('args', nargs='*')
        return options.set_options(parser)

    def take_action(self, parsed_args):
        args = vars(self.app.options)
        args.update(vars(parsed_args))
        s = ssh.SSH(settings.CONFIG_DIR, **args)
        s.ssh(args['host'], args['args'])
