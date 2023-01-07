from zbus_cli.command import CommandExtension
from zbus_cli.command import add_subparsers_on_demand


class TopicCommand(CommandExtension):
    """Various topic related sub-commands."""

    def add_arguments(self, parser, cli_name):
        self._subparser = parser

        # add arguments and sub-commands of verbs
        add_subparsers_on_demand(parser,
                                 cli_name,
                                 '_verb',
                                 'zbustopic.verb',
                                 required=False)

    def main(self, *, parser, args, addr):
        if not hasattr(args, '_verb'):
            # in case no verb was passed
            self._subparser.print_help()
            return 0

        extension = getattr(args, '_verb')

        # call the verb's main method
        return extension.main(args=args, addr=addr)
