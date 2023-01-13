import subprocess

import requests
from auterioncli.commands.command_base import CliCommand


class AppInitCommand(CliCommand):
    @staticmethod
    def help():
        return 'Initialize a new Auterion app repository'

    def needs_device(self, args):
        return False

    def __init__(self, config):
        pass

    def setup_parser(self, parser):
        pass

    def run(self, args):
        print('This command is not fully implemented yet.')
        print('For now, it will just git clone a C++ app template repository')
        print('')
        answer = input('> Clone app template repository into \'app-template-cpp\' folder? (yes, No)')
        if answer == 'yes':
            subprocess.run(['git', 'clone', 'git@github.com:Auterion/app-template-cpp.git'])
