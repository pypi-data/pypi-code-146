"""Module managing the argument parser"""
#      ubiquity
#      Copyright (C) 2022  INSA Rouen Normandie - CIP
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
import argparse
import sys
from typing import Optional, List

from . import __version__
from .version import check_new_version_client
from .controllers.config_file import Config
from .views.utils import gettext

_ = gettext.gettext


def _check_int(value) -> int:
    """Function checking if value is a positive int

    :param value: The value
    :raises ArgumentTypeError: The value is not a positive int
    :return: The int value
    """
    try:
        int_value = int(value)
    except ValueError as no_int:
        raise argparse.ArgumentTypeError(f"{_('invalid int value:')} {repr(value)}") from no_int
    if int_value <= 0:
        raise argparse.ArgumentTypeError(f"{_('invalid positive int value:')} {repr(value)}")
    return int_value


class ArgumentParser(argparse.ArgumentParser):
    """Class managing the argument parser"""
    def __init__(self):
        super().__init__()
        self.allow_abbrev = False
        self.usage = '%(prog)s [options]'
        self.description = _('Ubiquity-student allows the follow-up of computer science courses')
        self._optionals.title = _('Optional arguments')
        self._actions[0].help = _('show this help message and exit')
        self._add_arguments()
        self._args = self.parse_args()

    def _add_arguments(self):
        """Method adding all arguments"""
        self._add_basic_arguments()
        self._add_input_field_arguments()

    def _add_basic_arguments(self):
        """Method adding the basic arguments"""
        self.add_argument("-V", "--version", action="store_true", dest='version',
                          help=_("show the Ubiquity-student version number and exit"))
        mutually_exclusive_group = self.add_mutually_exclusive_group()
        mutually_exclusive_group.add_argument("-l", "--list", action="store_true", dest='list',
                                              help=_("show the configuration list and exit"))
        mutually_exclusive_group.add_argument("--load", type=_check_int, dest='load_id',
                                              help=_("load and run a configuration"))
        self.add_argument("-r", "--restore", action="store_true", dest='restore', default=False,
                          help=_("restore deleted files"))
        self.add_argument("--no-gui", action="store_true", dest='no_gui', default=False,
                          help=_("do not display the graphic user interface"))
        self.add_argument("--no-color", action="store_true", dest='no_color', default=False,
                          help=_("do not display colors on the console"))

    def _add_input_field_arguments(self):
        """Method adding the input field arguments"""
        group = self.add_argument_group(_('Input field'), _('If all values are defined, no form will be proposed'))
        group.add_argument("-s", "--server", type=str, dest='server',
                           help=_("define a value for the server field"))
        group.add_argument("-u", "--student-key", type=str, dest='student_key',
                           help=_("define a value for the student key field"))
        group.add_argument("-g", "--group-key", type=str, dest='group_key',
                           help=_("define a value for the group key field"))
        group.add_argument("-d", "--directory", type=str, dest='directory',
                           help=_("define a value for the directory field"))

    def execute_actions(self):
        """
        Method executes the different actions according to the arguments

        :return: The tuple containing the config, the values and the other parameters
        """
        self.version_action()
        config = Config()
        values = self._get_args_values()
        self.list_action(config, values)
        values = self.load_action(config, values)
        params = {
            'has_restore': self.restore_action(),
            'has_color': self.color_action(),
            'has_gui': self.gui_action(),
            'has_form': None in values,
            'has_new_version': check_new_version_client(self.color_action())
        }
        return config, values, params

    def version_action(self):
        """Method displaying the version and quit"""
        if self._args.version:
            print('Ubiquity-student ' + __version__)
            sys.exit(0)

    def list_action(self, config, values):
        """
        Method displaying the config list and quit

        :param config: The config
        :param values: The values
        """
        if self._args.list:
            servers = config.list_config(values)
            if len(servers) == 0:
                print('No practical work')
                sys.exit(0)
            for server in servers:
                print('Server: ' + server)
                for student_key in servers[server]:
                    print(' ' * 3 + 'Student key: ' + student_key)
                    for group_key in servers[server][student_key]:
                        print(' ' * 6 + '|' + '-' * 3 + '(' + servers[server][student_key][group_key]['id'] + ') ' +
                              'Group key: ' + group_key)
                        print(' ' * 6 + '|' + ' ' * 3 + 'Name: ' + servers[server][student_key][group_key][Config.NAME])
                        date = servers[server][student_key][group_key][Config.DATE]
                        if date:
                            print(' ' * 6 + '|' + ' ' * 3 + 'Date: ' + date)
                        print(' ' * 6 + '|' + ' ' * 3 + 'Directory: ' +
                              servers[server][student_key][group_key][Config.DIRECTORY])
                print()
            sys.exit(0)

    def load_action(self, config, values):
        """
        Method loading a config by an id or quit if not exists

        :param config: The config
        :param values: The values
        :return: The loaded values
        """
        if self._args.load_id:
            if self._args.server:
                self.error('argument -s/--server: not allowed with argument --load')
            if self._args.student_key:
                self.error('argument -u/--student_key: not allowed with argument --load')
            if self._args.group_key:
                self.error('argument -g/--group_key: not allowed with argument --load')
            if self._args.directory:
                self.error('argument -d/--directory: not allowed with argument --load')
            configs = config.configs.copy()
            configs.pop('default')
            key_list = list(configs)
            if len(key_list) >= self._args.load_id:
                config_values = configs[list(configs)[self._args.load_id-1]]
                config_server = config_values[config.SERVER]
                return [config_server,
                        config_values[config.STUDENT_KEY],
                        config_values[config.GROUP_KEY],
                        config_values[config.DIRECTORY]]
            print(f'No practical work with the id {self._args.load_id}')
            sys.exit(0)
        return values

    def restore_action(self):
        """
        Method setting the restore param

        :return: The restore value
        """
        if self._args.restore:
            if (not self._args.server or not self._args.student_key or not
               self._args.group_key or not self._args.directory) and not self._args.load_id:
                self.error('argument -r/--restore: Require with loading a configuration or entering all input fields')
            return True
        return False

    def color_action(self):
        """
        Method setting the color value

        :return: The color value
        """
        return not self._args.no_color

    def gui_action(self):
        """
        Method setting the GUI value

        :return: The GUI value
        """
        return not self._args.no_gui

    def _get_args_values(self) -> List[Optional[str]]:
        """Function returning the values list

        :return: The values list
        """
        return [self._args.server, self._args.student_key, self._args.group_key, self._args.directory]
