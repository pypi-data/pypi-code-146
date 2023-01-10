import requests
from auterioncli.commands.command_base import CliCommand
from .update import do_update
import os


def error(msg, code=1):
    print(msg)
    exit(code)


class AppInstallCommand(CliCommand):
    @staticmethod
    def help():
        return 'Install AuterionOS app to a connected device'

    def needs_device(self, args):
        return True

    def __init__(self, config):
        self._device_address = config['device_address']

    def setup_parser(self, parser):
        parser.add_argument('artifact', help='Artifact to install on the device', nargs='?', default='.')

    def run(self, args):
        artifact = args.artifact

        if os.path.exists(artifact) and os.path.isfile(artifact):
            print(f'Installing artifact {artifact}')
            do_update(artifact, self._device_address)

        else:
            error(f'No upload artifact at {artifact}. Exiting..')
