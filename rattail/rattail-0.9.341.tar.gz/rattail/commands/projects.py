# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2022 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Project Commands
"""

from __future__ import unicode_literals, absolute_import

import os
import subprocess
import sys

from rattail.commands.core import Subcommand
from rattail.projects.handler import RattailProjectHandler


class MakeProject(Subcommand):
    """
    Make a new app project
    """
    name = 'make-project'
    description = __doc__.strip()

    def add_parser_args(self, parser):
        parser.add_argument('path',
                            help="Path to project folder")

    def run(self, args):

        path = os.path.abspath(args.path)
        if os.path.exists(path):
            self.stderr.write("path already exists: {}\n".format(path))
            sys.exit(1)

        # nb. technically these would be required and auto-installed
        # as needed (later), but seems better to do this explicitly
        # up-front before any other command output
        self.require_prompt_toolkit()
        self.require_rich()

        # welcome, continue?
        self.rprint("\n\t[blue]Welcome to Rattail[/blue]")
        self.rprint("\n\tThis tool will generate source code for a new project.")
        if not self.basic_prompt("continue?", True, is_bool=True):
            self.rprint()
            sys.exit(0)

        # name
        name = os.path.basename(path)

        # app_table_prefix
        prefix = name
        prefix = prefix.replace('-', '_')
        prefix = prefix.replace(' ', '_')
        app_table_prefix = self.basic_prompt('app_table_prefix',
                                             default=prefix)
        app_table_prefix = app_table_prefix.rstrip('_')

        # app_class_prefix
        prefix = name
        prefix = prefix.replace('-', '_')
        prefix = prefix.replace('_', ' ')
        app_class_prefix = ''.join([w.capitalize() for w in prefix.split()])
        app_class_prefix = self.basic_prompt('app_class_prefix',
                                             default=app_class_prefix)

        # org_name
        org_name = self.basic_prompt('org_name', required=True)

        # pypi_name
        pypi_name = name
        pypi_name = pypi_name.replace('_', ' ')
        pypi_name = pypi_name.replace('-', ' ')
        pypi_name = '-'.join([w.capitalize()
                              for w in org_name.split() + pypi_name.split()])
        pypi_name = self.basic_prompt('pypi_name', default=pypi_name)

        # app_title
        app_title = name
        app_title = app_title.replace('-', ' ')
        app_title = app_title.replace('_', ' ')
        app_title = ' '.join([w.capitalize() for w in app_title.split()])

        # generate project
        project_handler = RattailProjectHandler(self.config)
        options = {
            'name': app_title,
            'slug': name,
            'organization': org_name,
            'python_project_name': pypi_name,
            'python_name': app_table_prefix,
            'has_db': True,
            'extends_db': True,
            'has_web': True,

            # TODO: these should not be needed..?
            'has_web_api': False,
            'has_datasync': False,
            'integrates_catapult': False,
            'integrates_corepos': False,
            'integrates_locsms': False,
            'uses_fabric': False,
        }
        project_handler.generate_project('rattail', name, options, path=path)
        self.rprint("\n\tproject created at:  [bold green]{}[/bold green]".format(
            path))

        # install pkg
        if self.basic_prompt("install project package?", is_bool=True, default=True):
            subprocess.check_call(['pip', 'install', '-e', path])
            self.rprint("\n\tpackage installed:  [bold green]{}[/bold green]".format(
                pypi_name))

            self.rprint("\n\tinstall and configure the app with:")
            self.rprint("\n\t[blue]{} -n install[/blue]".format(name))

        self.rprint()
