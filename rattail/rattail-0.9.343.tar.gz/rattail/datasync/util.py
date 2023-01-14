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
DataSync Utilities
"""

from __future__ import unicode_literals, absolute_import

import datetime
import warnings

import sqlalchemy as sa
from sqlalchemy import orm

from rattail.time import localtime, make_utc


def get_lastrun_setting(config, watcher_key):
    """
    Retrieve the "last run" setting name for the given watcher key.
    """
    warnings.warn("get_lastrun_setting() function is deprecated; please use "
                  "DatasyncHandler.get_watcher_lastrun_setting() method instead",
                  DeprecationWarning, stacklevel=2)

    app = config.get_app()
    handler = app.get_datasync_handler()
    return handler.get_watcher_lastrun_setting(watcher_key)


def get_lastrun_timefmt(config):
    """
    Retrieve the "last run" time format.
    """
    warnings.warn("get_lastrun_timefmt() function is deprecated; please use "
                  "DatasyncHandler.get_lastrun_timefmt() method instead",
                  DeprecationWarning, stacklevel=2)

    app = config.get_app()
    handler = app.get_datasync_handler()
    return handler.get_lastrun_timefmt()


def get_lastrun(config, watcher_key, **kwargs):
    """
    Retrieve the "last run" time for the datasync watcher thread identifed by
    ``watcher_key``.
    """
    warnings.warn("get_lastrun() function is deprecated; please use "
                  "DatasyncHandler.get_watcher_lastrunrun() method instead",
                  DeprecationWarning, stacklevel=2)

    app = config.get_app()
    handler = app.get_datasync_handler()
    return handler.get_watcher_lastrun(watcher_key, **kwargs)


def make_dependency_sorter(model):
    """
    Return a function suitable for use when sorting data model class names,
    according to the underlying foreign key dependencies between the tables.
    """

    def depends_on(mapper_x, mapper_y, visited=set()):
        """
        Returns True if model 'x' has a (in)direct FK dependency on 'y', else False.
        """
        # First check for direct FK dependency.
        for column in mapper_x.columns:
            for fkey in column.foreign_keys:
                if fkey.column.table in mapper_y.tables:
                    return True

        # Must keep track of where we're been, to avoid infinite recursion in
        # the case of mutually-dependent tables.
        visited.add(mapper_x)

        # Next check recursively, for indirect FK dependency.
        for prop in mapper_x.iterate_properties:
            if isinstance(prop, orm.RelationshipProperty):
                if prop.direction.name == 'MANYTOONE':
                    if prop.mapper not in visited:
                        if depends_on(prop.mapper, mapper_y, visited=visited):
                            return True

        return False

    def dependency_sorter(x, y):
        """
        This function is meant to be used as the ``cmp`` kwarg to a standard
        Python sorting function.
        """
        map_x = orm.class_mapper(getattr(model, x))
        map_y = orm.class_mapper(getattr(model, y))

        # Check to see if one model depends (in)directly on the other.  If "x
        # depends on y" then we consider "x > y" and hence the final sort
        # result would be (y, x).  Note however that in the case of mutually
        # dependent tables, we must remain neutral and allow the tie.
        dep_x = depends_on(map_x, map_y)
        dep_y = depends_on(map_y, map_x)
        if dep_x and not dep_y:
            return 1
        if dep_y and not dep_x:
            return -1
        return 0

    return dependency_sorter


def next_batch_id(session):
    """
    Return the next "batch ID" for datasync changes, for use when recording by
    a watcher thread.
    """
    sql = "select nextval('datasync_change_batch_id_seq')"
    return session.execute(sql).scalar()


def purge_datasync_settings(config, session):
    app = config.get_app()
    model = config.get_model()

    to_delete = session.query(model.Setting)\
                       .filter(sa.or_(
                           model.Setting.name == 'rattail.datasync.watch',
                           model.Setting.name == 'rattail.datasync.supervisor_process_name',
                           model.Setting.name == 'rattail.datasync.use_profile_settings',
                           model.Setting.name == 'tailbone.datasync.restart',
                           model.Setting.name.like('rattail.datasync.%.watcher'),
                           model.Setting.name.like('rattail.datasync.%.watcher.db'),
                           model.Setting.name.like('rattail.datasync.%.watcher.delay'),
                           model.Setting.name.like('rattail.datasync.%.watcher.retry_attempts'),
                           model.Setting.name.like('rattail.datasync.%.watcher.retry_delay'),
                           model.Setting.name.like('rattail.datasync.%.watcher.kwarg.%'),
                           model.Setting.name.like('rattail.datasync.%.consumers'),
                           model.Setting.name.like('rattail.datasync.%.consumers.runas'),
                           model.Setting.name.like('rattail.datasync.%.consumer.%')))\
                       .all()
    for setting in to_delete:
        app.delete_setting(session, setting.name)
