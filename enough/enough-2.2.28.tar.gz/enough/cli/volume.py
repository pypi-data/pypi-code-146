from cliff.command import Command

from enough import settings
from enough.common import Enough
from enough.common import options


class Resize(Command):
    "Resize a volume"

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('host')
        parser.add_argument('volume')
        return options.set_options(parser)

    def take_action(self, parsed_args):
        args = vars(self.app.options)
        args.update(vars(parsed_args))
        e = Enough(settings.CONFIG_DIR, settings.SHARE_DIR, **args)
        e.volume_resize(args['host'], args['volume'])
