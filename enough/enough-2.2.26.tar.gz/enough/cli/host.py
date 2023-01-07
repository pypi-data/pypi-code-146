from cliff.show import ShowOne
from cliff.command import Command

from enough import settings
from enough.common import Enough
from enough.common import options


class Create(ShowOne):
    "Create or update a host"

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('name')
        return options.set_options(parser)

    def take_action(self, parsed_args):
        args = vars(self.app.options)
        args.update(vars(parsed_args))
        e = Enough(settings.CONFIG_DIR, settings.SHARE_DIR, **args)
        r = e.host.create_or_update()
        columns = ('name', 'user', 'port', 'ip')
        data = (parsed_args.name, 'debian', r['port'], r['ipv4'])
        return (columns, data)


class Delete(Command):
    "Delete a host"

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('name', nargs='+')
        return options.set_options(parser)

    def take_action(self, parsed_args):
        args = vars(self.app.options)
        args.update(vars(parsed_args))
        e = Enough(settings.CONFIG_DIR, settings.SHARE_DIR, **args)
        e.host.delete()
