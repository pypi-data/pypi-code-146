# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
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
Database Handler
"""

from __future__ import unicode_literals, absolute_import

from alembic.config import Config as AlembicConfig
from alembic.script import ScriptDirectory
from mako.lookup import TemplateLookup

from rattail.app import GenericHandler
from rattail.files import resource_path


class DatabaseHandler(GenericHandler):
    """
    Base class and default implementation for the DB handler.
    """

    def __init__(self, *args, **kwargs):
        super(DatabaseHandler, self).__init__(*args, **kwargs)

        # TODO: make templates dir configurable?
        templates = [resource_path('rattail:templates/db')]
        self.templates = TemplateLookup(directories=templates)

    def get_alembic_branch_names(self, **kwargs):
        """
        Returns a list of Alembic branch names present in the default
        database schema.
        """
        alembic_config = AlembicConfig()
        alembic_config.set_main_option(
            'script_location',
            self.config.get('alembic', 'script_location', usedb=False))
        alembic_config.set_main_option(
            'version_locations',
            self.config.get('alembic', 'version_locations', usedb=False))

        script = ScriptDirectory.from_config(alembic_config)

        branches = set()
        for rev in script.get_revisions(script.get_heads()):
            branches.update(rev.branch_labels)

        return sorted(branches)

    def write_table_model(self, data, path, **kwargs):
        """
        Write code for a new table model, based on the given data
        dict, to the given path.
        """
        template = self.templates.get_template('/new-table.mako')
        content = template.render(**data)
        with open(path, 'wt') as f:
            f.write(content)
