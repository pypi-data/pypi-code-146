from cliff.command import Command

from enough import settings
from enough.common import options
from enough.common import Enough


class Info(Command):
    "Display information about the Enough instance"

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--show-passwords',
                            action='store_true',
                            help='show actual passwords instead of placeholders')
        return options.set_options(parser)

    def take_action(self, parsed_args):
        args = vars(self.app.options)
        args.update(vars(parsed_args))
        e = Enough(settings.CONFIG_DIR, settings.SHARE_DIR, **args)
        print("\n".join(e.info()) + "\n")
