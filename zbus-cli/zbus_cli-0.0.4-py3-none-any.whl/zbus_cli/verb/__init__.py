class VerbExtension:
    """
    The extension point for 'topic' verb extensions.

    The following properties must be defined:
    * `NAME` (will be set to the entry point name)

    The following methods must be defined:
    * `main`

    The following methods can be defined:
    * `add_arguments`
    """

    NAME = None
    EXTENSION_POINT_VERSION = '0.1'

    def __init__(self):
        super(VerbExtension, self).__init__()

    def add_arguments(self, parser, cli_name):
        pass

    def main(self, *, args, addr):
        raise NotImplementedError()