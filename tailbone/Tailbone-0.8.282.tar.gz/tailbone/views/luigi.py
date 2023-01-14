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
Views for Luigi
"""

from __future__ import unicode_literals, absolute_import

import json
import logging
import os
import re
import shlex

import six
import sqlalchemy as sa

from rattail.util import simple_error

from tailbone.views import MasterView


log = logging.getLogger(__name__)


class LuigiTaskView(MasterView):
    """
    Simple views for Luigi tasks.
    """
    normalized_model_name = 'luigitasks'
    model_key = 'key'
    model_title = "Luigi Task"
    route_prefix = 'luigi'
    url_prefix = '/luigi'

    viewable = False
    creatable = False
    editable = False
    deletable = False
    configurable = True

    def __init__(self, request, context=None):
        super(LuigiTaskView, self).__init__(request, context=context)
        app = self.get_rattail_app()

        # nb. luigi may not be installed, which (for now) may prevent
        # us from getting our handler; in which case warn user
        try:
            self.luigi_handler = app.get_luigi_handler()
        except Exception as error:
            self.luigi_handler = None
            self.luigi_handler_error = error
            log.warning("could not get luigi handler", exc_info=True)

    def index(self):

        if not self.luigi_handler:
            self.request.session.flash("Could not create handler: {}".format(
                simple_error(self.luigi_handler_error)), 'error')

        luigi_url = self.rattail_config.get('rattail.luigi', 'url')
        history_url = '{}/history'.format(luigi_url.rstrip('/')) if luigi_url else None
        return self.render_to_response('index', {
            'use_buefy': self.get_use_buefy(),
            'index_url': None,
            'luigi_url': luigi_url,
            'luigi_history_url': history_url,
            'overnight_tasks': self.get_overnight_tasks(),
            'backfill_tasks': self.get_backfill_tasks(),
        })

    def launch_overnight(self):
        app = self.get_rattail_app()
        data = self.request.json_body

        key = data.get('key')
        task = self.luigi_handler.get_overnight_task(key) if key else None
        if not task:
            return self.json_response({'error': "Task not found"})

        try:
            self.luigi_handler.launch_overnight_task(task, app.yesterday(),
                                                     keep_config=False,
                                                     email_if_empty=True,
                                                     wait=False)
        except Exception as error:
            log.warning("failed to launch overnight task: %s", task,
                        exc_info=True)
            return self.json_response({'error': simple_error(error)})
        return self.json_response({'ok': True})

    def launch_backfill(self):
        app = self.get_rattail_app()
        data = self.request.json_body

        key = data.get('key')
        task = self.luigi_handler.get_backfill_task(key) if key else None
        if not task:
            return self.json_response({'error': "Task not found"})

        start_date = app.parse_date(data['start_date'])
        end_date = app.parse_date(data['end_date'])
        try:
            self.luigi_handler.launch_backfill_task(task, start_date, end_date)
        except Exception as error:
            log.warning("failed to launch backfill task: %s", task,
                        exc_info=True)
            return self.json_response({'error': simple_error(error)})
        return self.json_response({'ok': True})

    def restart_scheduler(self):
        try:
            self.luigi_handler.restart_supervisor_process()
            self.request.session.flash("Luigi scheduler has been restarted.")

        except Exception as error:
            log.warning("restart failed", exc_info=True)
            self.request.session.flash(simple_error(error), 'error')

        return self.redirect(self.request.get_referrer(
            default=self.get_index_url()))

    def configure_get_simple_settings(self):
        return [

            # luigi proper
            {'section': 'rattail.luigi',
             'option': 'url'},
            {'section': 'rattail.luigi',
             'option': 'scheduler.supervisor_process_name'},
            {'section': 'rattail.luigi',
             'option': 'scheduler.restart_command'},

        ]

    def configure_get_context(self, **kwargs):
        context = super(LuigiTaskView, self).configure_get_context(**kwargs)
        context['overnight_tasks'] = self.get_overnight_tasks()
        context['backfill_tasks'] = self.get_backfill_tasks()
        return context

    def get_overnight_tasks(self):
        if self.luigi_handler:
            tasks = self.luigi_handler.get_all_overnight_tasks()
        else:
            tasks = []
        for task in tasks:
            if task['last_date']:
                task['last_date'] = six.text_type(task['last_date'])
        return tasks

    def get_backfill_tasks(self):
        if self.luigi_handler:
            tasks = self.luigi_handler.get_all_backfill_tasks()
        else:
            tasks = []
        for task in tasks:
            if task['last_date']:
                task['last_date'] = six.text_type(task['last_date'])
            if task['target_date']:
                task['target_date'] = six.text_type(task['target_date'])
        return tasks

    def configure_gather_settings(self, data):
        settings = super(LuigiTaskView, self).configure_gather_settings(data)
        app = self.get_rattail_app()

        # overnight tasks
        keys = []
        for task in json.loads(data['overnight_tasks']):
            key = task['key']
            keys.append(key)
            settings.extend([
                {'name': 'rattail.luigi.overnight.task.{}.description'.format(key),
                 'value': task['description']},
                {'name': 'rattail.luigi.overnight.task.{}.module'.format(key),
                 'value': task['module']},
                {'name': 'rattail.luigi.overnight.task.{}.class_name'.format(key),
                 'value': task['class_name']},
                {'name': 'rattail.luigi.overnight.task.{}.script'.format(key),
                 'value': task['script']},
                {'name': 'rattail.luigi.overnight.task.{}.notes'.format(key),
                 'value': task['notes']},
            ])
        if keys:
            settings.append({'name': 'rattail.luigi.overnight.tasks',
                             'value': ', '.join(keys)})

        # backfill tasks
        keys = []
        for task in json.loads(data['backfill_tasks']):
            key = task['key']
            keys.append(key)
            settings.extend([
                {'name': 'rattail.luigi.backfill.task.{}.description'.format(key),
                 'value': task['description']},
                {'name': 'rattail.luigi.backfill.task.{}.script'.format(key),
                 'value': task['script']},
                {'name': 'rattail.luigi.backfill.task.{}.forward'.format(key),
                 'value': 'true' if task['forward'] else 'false'},
                {'name': 'rattail.luigi.backfill.task.{}.notes'.format(key),
                 'value': task['notes']},
                {'name': 'rattail.luigi.backfill.task.{}.target_date'.format(key),
                 'value': six.text_type(task['target_date'])},
            ])
        if keys:
            settings.append({'name': 'rattail.luigi.backfill.tasks',
                             'value': ', '.join(keys)})

        return settings

    def configure_remove_settings(self):
        super(LuigiTaskView, self).configure_remove_settings()

        self.luigi_handler.purge_overnight_settings(self.Session())
        self.luigi_handler.purge_backfill_settings(self.Session())

    @classmethod
    def defaults(cls, config):
        cls._defaults(config)
        cls._luigi_defaults(config)

    @classmethod
    def _luigi_defaults(cls, config):
        route_prefix = cls.get_route_prefix()
        permission_prefix = cls.get_permission_prefix()
        url_prefix = cls.get_url_prefix()
        model_title_plural = cls.get_model_title_plural()

        # launch overnight
        config.add_tailbone_permission(permission_prefix,
                                       '{}.launch_overnight'.format(permission_prefix),
                                       label="Launch any Overnight Task")
        config.add_route('{}.launch_overnight'.format(route_prefix),
                         '{}/launch-overnight'.format(url_prefix),
                         request_method='POST')
        config.add_view(cls, attr='launch_overnight',
                        route_name='{}.launch_overnight'.format(route_prefix),
                        permission='{}.launch_overnight'.format(permission_prefix))

        # launch backfill
        config.add_tailbone_permission(permission_prefix,
                                       '{}.launch_backfill'.format(permission_prefix),
                                       label="Launch any Backfill Task")
        config.add_route('{}.launch_backfill'.format(route_prefix),
                         '{}/launch-backfill'.format(url_prefix),
                         request_method='POST')
        config.add_view(cls, attr='launch_backfill',
                        route_name='{}.launch_backfill'.format(route_prefix),
                        permission='{}.launch_backfill'.format(permission_prefix))

        # restart luigid scheduler
        config.add_tailbone_permission(permission_prefix,
                                       '{}.restart_scheduler'.format(permission_prefix),
                                       label="Restart the Luigi Scheduler daemon")
        config.add_route('{}.restart_scheduler'.format(route_prefix),
                         '{}/restart-scheduler'.format(url_prefix),
                         request_method='POST')
        config.add_view(cls, attr='restart_scheduler',
                        route_name='{}.restart_scheduler'.format(route_prefix),
                        permission='{}.restart_scheduler'.format(permission_prefix))


def defaults(config, **kwargs):
    base = globals()

    LuigiTaskView = kwargs.get('LuigiTaskView', base['LuigiTaskView'])
    LuigiTaskView.defaults(config)


def includeme(config):
    defaults(config)
