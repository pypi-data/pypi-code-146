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
Views with info about the underlying Rattail tables
"""

from __future__ import unicode_literals, absolute_import

import sys
import warnings

import colander
from deform import widget as dfwidget

from tailbone.views import MasterView


class TableView(MasterView):
    """
    Master view for tables
    """
    normalized_model_name = 'table'
    model_key = 'table_name'
    model_title = "Table"
    creatable = False
    editable = False
    deletable = False
    filterable = False
    pageable = False

    labels = {
        'branch_name': "Schema Branch",
        'model_name': "Model Class",
        'module_name': "Module",
        'module_file': "File",
    }

    grid_columns = [
        'table_name',
        'row_count',
    ]

    def __init__(self, request):
        super(TableView, self).__init__(request)
        app = self.get_rattail_app()
        self.db_handler = app.get_db_handler()

    def get_data(self, **kwargs):
        """
        Fetch existing table names and estimate row counts via PG SQL
        """
        # note that we only show 'public' schema tables, i.e. avoid the 'batch'
        # schema, at least for now?  maybe should include all, plus show the
        # schema name within the results grid?
        sql = """
        select relname, n_live_tup
        from pg_stat_user_tables
        where schemaname = 'public'
        order by n_live_tup desc;
        """
        result = self.Session.execute(sql)
        return [dict(table_name=row['relname'], row_count=row['n_live_tup'])
                for row in result]

    def configure_grid(self, g):
        super(TableView, self).configure_grid(g)

        # table_name
        g.sorters['table_name'] = g.make_simple_sorter('table_name', foldcase=True)
        g.set_sort_defaults('table_name')
        g.set_searchable('table_name')
        g.set_link('table_name')

        # row_count
        g.sorters['row_count'] = g.make_simple_sorter('row_count')

    def get_instance(self):
        from sqlalchemy_utils import get_mapper

        model = self.model
        table_name = self.request.matchdict['table_name']

        sql = """
        select n_live_tup
        from pg_stat_user_tables
        where schemaname = 'public' and relname = :table_name
        order by n_live_tup desc;
        """
        result = self.Session.execute(sql, {'table_name': table_name})
        row = result.fetchone()
        if not row:
            raise self.notfound()

        data = {
            'table_name': table_name,
            'row_count': row['n_live_tup'],
        }

        table = model.Base.metadata.tables.get(table_name)
        if table is not None:
            try:
                mapper = get_mapper(table)
            except ValueError:
                pass
            else:
                data['model_name'] = mapper.class_.__name__
                data['model_title'] = mapper.class_.get_model_title()
                data['model_title_plural'] = mapper.class_.get_model_title_plural()
                data['description'] = mapper.class_.__doc__

                # TODO: how to reliably get branch?  must walk all revisions?
                module_parts = mapper.class_.__module__.split('.')
                data['branch_name'] = module_parts[0]

                data['module_name'] = mapper.class_.__module__
                data['module_file'] = sys.modules[mapper.class_.__module__].__file__

        return data

    def get_instance_title(self, table):
        return table['table_name']

    def make_form_schema(self):
        return TableSchema()

    def configure_form(self, f):
        super(TableView, self).configure_form(f)
        app = self.get_rattail_app()

        # exclude some fields when creating
        if self.creating:
            f.remove('row_count',
                     'module_name',
                     'module_file')

        # branch_name
        if self.creating:

            # move this field to top of form, as it's more fundamental
            # when creating new table
            f.remove('branch_name')
            f.insert(0, 'branch_name')

            # define options for dropdown
            branches = self.db_handler.get_alembic_branch_names()
            values = [(branch, branch) for branch in branches]
            f.set_widget('branch_name', dfwidget.SelectWidget(values=values))

            # default to custom app branch, if applicable
            table_prefix = app.get_table_prefix()
            if table_prefix in branches:
                f.set_default('branch_name', table_prefix)
                f.set_helptext('branch_name', "Leave this set to your custom app branch, unless you know what you're doing.")

        # table_name
        if self.creating:
            f.set_default('table_name', '{}_widget'.format(app.get_table_prefix()))
            f.set_helptext('table_name', "Should be singular in nature, i.e. 'widget' not 'widgets'")

        # model_name
        if self.creating:
            f.set_default('model_name', '{}Widget'.format(app.get_class_prefix()))
            f.set_helptext('model_name', "Should be singular in nature, i.e. 'Widget' not 'Widgets'")

        # model_title*
        if self.creating:
            f.set_default('model_title', 'Widget')
            f.set_helptext('model_title', "Human-friendly singular model title.")
            f.set_default('model_title_plural', 'Widgets')
            f.set_helptext('model_title_plural', "Human-friendly plural model title.")

        # description
        if self.creating:
            f.set_default('description', "Represents a cool widget.")
            f.set_helptext('description', "Brief description of what a record in this table represents.")

    # TODO: not sure yet how to handle "save" action
    # def save_create_form(self, form):
    #     return form.validated

    @classmethod
    def defaults(cls, config):
        rattail_config = config.registry.settings.get('rattail_config')

        # allow creating tables only if *not* production
        if not rattail_config.production():
            cls.creatable = True

        cls._defaults(config)


class TablesView(TableView):

    def __init__(self, request):
        warnings.warn("TablesView is deprecated; please use TableView instead",
                      DeprecationWarning, stacklevel=2)
        super(TablesView, self).__init__(request)


class TableSchema(colander.Schema):

    table_name = colander.SchemaNode(colander.String())

    row_count = colander.SchemaNode(colander.Integer(),
                                    missing=colander.null)

    model_name = colander.SchemaNode(colander.String())

    model_title = colander.SchemaNode(colander.String())

    model_title_plural = colander.SchemaNode(colander.String())

    description = colander.SchemaNode(colander.String())

    branch_name = colander.SchemaNode(colander.String())

    module_name = colander.SchemaNode(colander.String(),
                                      missing=colander.null)

    module_file = colander.SchemaNode(colander.String(),
                                      missing=colander.null)


def defaults(config, **kwargs):
    base = globals()

    TableView = kwargs.get('TableView', base['TableView'])
    TableView.defaults(config)


def includeme(config):
    defaults(config)
