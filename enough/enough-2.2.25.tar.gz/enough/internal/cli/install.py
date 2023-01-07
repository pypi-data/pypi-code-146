import jinja2
import logging
import os

from cliff.command import Command
from enough.version import __version__


class InstallScript(Command):
    "Get scripts, systemd services etc. required to run Enough."

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InstallScript, self).get_parser(prog_name)
        group_registry = parser.add_mutually_exclusive_group()
        group_registry.add_argument('--registry', default='enoughcommunity/')
        group_registry.add_argument('--no-registry', action='store_true')
        parser.add_argument('--function', action='store_true')
        group_tag = parser.add_mutually_exclusive_group()
        group_tag.add_argument('--tag', default=__version__)
        group_tag.add_argument('--no-tag', action='store_true')
        parser.add_argument('--no-tty', action='store_true')
        parser.add_argument('path', nargs='?')
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.path:
            path = 'internal/data/install.sh'
            function = True
        else:
            path = parsed_args.path
            function = parsed_args.function
        self.args = parsed_args
        if parsed_args.no_registry:
            self.registry = ''
        else:
            self.registry = parsed_args.registry
        if parsed_args.no_tty:
            self.tty = ''
        else:
            self.tty = '-ti'
        if parsed_args.no_tag:
            self.tag = ''
        else:
            self.tag = f':{parsed_args.tag}'
        i = os.path.join(os.path.dirname(__file__), '../..', path)
        content = open(i).read()
        if function:
            content = 'function enough() {' + content + '}'
        print(jinja2.Template(content).render(this=self))
