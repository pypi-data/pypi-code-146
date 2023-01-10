from cliff.show import ShowOne

from enough import settings
from enough.common import options
from enough.common import Enough


class Create(ShowOne):
    "Create or update a service"

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('name')
        parser.add_argument('--playbook', default='enough-playbook.yml')
        parser.add_argument('--host')
        return options.set_options(parser)

    def take_action(self, parsed_args):
        args = vars(self.app.options)
        args.update(vars(parsed_args))
        e = Enough(settings.CONFIG_DIR, settings.SHARE_DIR, **args)
        r = e.service.create_or_update()
        columns = ('name',)
        data = (r['fqdn'],)
        return (columns, data)
