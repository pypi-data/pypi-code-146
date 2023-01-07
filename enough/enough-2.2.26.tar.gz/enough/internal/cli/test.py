from cliff.show import ShowOne
from enough import settings
from enough.common import openstack


class CreateTestSubdomain(ShowOne):
    "Create and delegate a test subdomain, if possible"

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('apidomain', help='will send the creation request to api.{apidomain}')
        return parser

    def take_action(self, parsed_args):
        h = openstack.Heat(settings.CONFIG_DIR)
        r = h.create_test_subdomain(parsed_args.apidomain)
        columns = ('name',)
        data = (r,)
        return (columns, data)
