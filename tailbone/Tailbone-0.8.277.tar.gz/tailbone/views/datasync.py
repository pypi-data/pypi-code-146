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
DataSync Views
"""

from __future__ import unicode_literals, absolute_import

import json
import subprocess
import logging

import six
import sqlalchemy as sa

from rattail.db import model
from rattail.datasync.util import purge_datasync_settings
from rattail.util import simple_error

from tailbone.views import MasterView
from tailbone.util import raw_datetime
from tailbone.config import should_expose_websockets


log = logging.getLogger(__name__)


class DataSyncThreadView(MasterView):
    """
    Master view for DataSync itself.

    This should (eventually) show all running threads in the main
    index view, with status for each, sort of akin to "dashboard".
    For now it only serves the config view.
    """
    model_title = "DataSync Thread"
    model_title_plural = "DataSync Status"
    model_key = 'key'
    route_prefix = 'datasync'
    url_prefix = '/datasync'
    listable = False
    viewable = False
    creatable = False
    editable = False
    deletable = False
    filterable = False
    pageable = False

    configurable = True
    config_title = "DataSync"

    grid_columns = [
        'key',
    ]

    def __init__(self, request, context=None):
        super(DataSyncThreadView, self).__init__(request, context=context)
        app = self.get_rattail_app()
        self.datasync_handler = app.get_datasync_handler()

    def status(self):
        """
        View to list/filter/sort the model data.

        If this view receives a non-empty 'partial' parameter in the query
        string, then the view will return the rendered grid only.  Otherwise
        returns the full page.
        """
        app = self.get_rattail_app()
        model = self.model

        try:
            process_info = self.datasync_handler.get_supervisor_process_info()
            supervisor_error = None
        except Exception as error:
            log.warning("failed to get supervisor process info", exc_info=True)
            process_info = None
            supervisor_error = simple_error(error)

        try:
            profiles = self.datasync_handler.get_configured_profiles()
        except Exception as error:
            log.warning("could not load profiles!", exc_info=True)
            self.request.session.flash(simple_error(error), 'error')
            profiles = {}

        sql = """
        select source, consumer, count(*) as changes
        from datasync_change
        group by source, consumer
        """
        result = self.Session.execute(sql)
        all_changes = {}
        for row in result:
            all_changes[(row.source, row.consumer)] = row.changes

        watcher_data = []
        consumer_data = []
        now = app.localtime()
        for key, profile in six.iteritems(profiles):
            watcher = profile.watcher

            lastrun = self.datasync_handler.get_watcher_lastrun(
                watcher.key, local=True, session=self.Session())

            status = "okay"
            if (now - lastrun).total_seconds() >= (watcher.delay * 2):
                status = "dead watcher"

            watcher_data.append({
                'key': watcher.key,
                'spec': profile.watcher_spec,
                'dbkey': watcher.dbkey,
                'delay': watcher.delay,
                'lastrun': raw_datetime(self.rattail_config, lastrun, verbose=True),
                'status': status,
            })

            for consumer in profile.consumers:
                if consumer.watcher is watcher:

                    changes = all_changes.get((watcher.key, consumer.key), 0)
                    if changes:
                        oldest = self.Session.query(sa.func.min(model.DataSyncChange.obtained))\
                                             .filter(model.DataSyncChange.source == watcher.key)\
                                             .filter(model.DataSyncChange.consumer == consumer.key)\
                                             .scalar()
                        oldest = app.localtime(oldest, from_utc=True)
                        changes = "{} (oldest from {})".format(
                            changes,
                            app.render_time_ago(now - oldest))

                    status = "okay"
                    if changes:
                        status = "processing changes"

                    consumer_data.append({
                        'key': '{} -> {}'.format(watcher.key, consumer.key),
                        'spec': consumer.spec,
                        'dbkey': consumer.dbkey,
                        'delay': consumer.delay,
                        'changes': changes,
                        'status': status,
                    })

        watcher_data.sort(key=lambda w: w['key'])
        consumer_data.sort(key=lambda c: c['key'])

        context = {
            'index_title': "DataSync Status",
            'index_url': None,
            'process_info': process_info,
            'supervisor_error': supervisor_error,
            'watcher_data': watcher_data,
            'consumer_data': consumer_data,
        }
        return self.render_to_response('status', context)

    def get_data(self, session=None):
        data = []
        return data

    def restart(self):
        try:
            self.datasync_handler.restart_supervisor_process()
            self.request.session.flash("DataSync daemon has been restarted.")

        except Exception as error:
            self.request.session.flash(simple_error(error), 'error')

        return self.redirect(self.request.get_referrer(
            default=self.request.route_url('datasyncchanges')))

    def configure_get_context(self):
        profiles = self.datasync_handler.get_configured_profiles(
            include_disabled=True,
            ignore_problems=True)

        profiles_data = []
        for profile in sorted(profiles.values(), key=lambda p: p.key):
            data = {
                'key': profile.key,
                'watcher_spec': profile.watcher_spec,
                'watcher_dbkey': profile.watcher.dbkey,
                'watcher_delay': profile.watcher.delay,
                'watcher_retry_attempts': profile.watcher.retry_attempts,
                'watcher_retry_delay': profile.watcher.retry_delay,
                'watcher_default_runas': profile.watcher.default_runas,
                'watcher_consumes_self': profile.watcher.consumes_self,
                'watcher_kwargs_data': [{'key': key,
                                         'value': profile.watcher_kwargs[key]}
                                        for key in sorted(profile.watcher_kwargs)],
                # 'notes': None,   # TODO
                'enabled': profile.enabled,
            }

            consumers = []
            if profile.watcher.consumes_self:
                pass
            else:
                for consumer in sorted(profile.consumers, key=lambda c: c.key):
                    consumers.append({
                        'key': consumer.key,
                        'consumer_spec': consumer.spec,
                        'consumer_dbkey': consumer.dbkey,
                        'consumer_runas': getattr(consumer, 'runas', None),
                        'consumer_delay': consumer.delay,
                        'consumer_retry_attempts': consumer.retry_attempts,
                        'consumer_retry_delay': consumer.retry_delay,
                        'enabled': consumer.enabled,
                    })
            data['consumers_data'] = consumers
            profiles_data.append(data)

        return {
            'profiles': profiles,
            'profiles_data': profiles_data,
            'use_profile_settings': self.datasync_handler.should_use_profile_settings(),
            'supervisor_process_name': self.rattail_config.get(
                'rattail.datasync', 'supervisor_process_name'),
            'restart_command': self.rattail_config.get(
                'tailbone', 'datasync.restart'),
        }

    def configure_gather_settings(self, data):
        settings = []
        watch = []

        use_profile_settings = data.get('use_profile_settings') == 'true'
        settings.append({'name': 'rattail.datasync.use_profile_settings',
                         'value': 'true' if use_profile_settings else 'false'})

        if use_profile_settings:

            for profile in json.loads(data['profiles']):
                pkey = profile['key']
                if profile['enabled']:
                    watch.append(pkey)

                settings.extend([
                    {'name': 'rattail.datasync.{}.watcher'.format(pkey),
                     'value': profile['watcher_spec']},
                    {'name': 'rattail.datasync.{}.watcher.db'.format(pkey),
                     'value': profile['watcher_dbkey']},
                    {'name': 'rattail.datasync.{}.watcher.delay'.format(pkey),
                     'value': profile['watcher_delay']},
                    {'name': 'rattail.datasync.{}.watcher.retry_attempts'.format(pkey),
                     'value': profile['watcher_retry_attempts']},
                    {'name': 'rattail.datasync.{}.watcher.retry_delay'.format(pkey),
                     'value': profile['watcher_retry_delay']},
                    {'name': 'rattail.datasync.{}.consumers.runas'.format(pkey),
                     'value': profile['watcher_default_runas']},
                ])

                for kwarg in profile['watcher_kwargs_data']:
                    settings.append({
                        'name': 'rattail.datasync.{}.watcher.kwarg.{}'.format(
                            pkey, kwarg['key']),
                        'value': kwarg['value'],
                    })

                consumers = []
                if profile['watcher_consumes_self']:
                    consumers = ['self']
                else:

                    for consumer in profile['consumers_data']:
                        ckey = consumer['key']
                        if consumer['enabled']:
                            consumers.append(ckey)
                        settings.extend([
                            {'name': 'rattail.datasync.{}.consumer.{}'.format(pkey, ckey),
                             'value': consumer['consumer_spec']},
                            {'name': 'rattail.datasync.{}.consumer.{}.db'.format(pkey, ckey),
                             'value': consumer['consumer_dbkey']},
                            {'name': 'rattail.datasync.{}.consumer.{}.delay'.format(pkey, ckey),
                             'value': consumer['consumer_delay']},
                            {'name': 'rattail.datasync.{}.consumer.{}.retry_attempts'.format(pkey, ckey),
                             'value': consumer['consumer_retry_attempts']},
                            {'name': 'rattail.datasync.{}.consumer.{}.retry_delay'.format(pkey, ckey),
                             'value': consumer['consumer_retry_delay']},
                            {'name': 'rattail.datasync.{}.consumer.{}.runas'.format(pkey, ckey),
                             'value': consumer['consumer_runas']},
                        ])

                settings.extend([
                    {'name': 'rattail.datasync.{}.consumers'.format(pkey),
                     'value': ', '.join(consumers)},
                ])

            if watch:
                settings.append({'name': 'rattail.datasync.watch',
                                 'value': ', '.join(watch)})

        if data['supervisor_process_name']:
            settings.append({'name': 'rattail.datasync.supervisor_process_name',
                             'value': data['supervisor_process_name']})

        if data['restart_command']:
            settings.append({'name': 'tailbone.datasync.restart',
                             'value': data['restart_command']})

        return settings

    def configure_remove_settings(self):
        purge_datasync_settings(self.rattail_config, self.Session())

    @classmethod
    def defaults(cls, config):
        cls._defaults(config)
        cls._datasync_defaults(config)

    @classmethod
    def _datasync_defaults(cls, config):
        permission_prefix = cls.get_permission_prefix()
        route_prefix = cls.get_route_prefix()
        url_prefix = cls.get_url_prefix()
        index_title = cls.get_index_title()

        # view status
        config.add_tailbone_permission(permission_prefix,
                                       '{}.status'.format(permission_prefix),
                                       "View status for DataSync daemon")
        # nb. simple 'datasync' route points to 'datasync.status' for now..
        config.add_route(route_prefix,
                         '{}/status/'.format(url_prefix))
        config.add_route('{}.status'.format(route_prefix),
                         '{}/status/'.format(url_prefix))
        config.add_view(cls, attr='status',
                        route_name=route_prefix,
                        permission='{}.status'.format(permission_prefix))
        config.add_view(cls, attr='status',
                        route_name='{}.status'.format(route_prefix),
                        permission='{}.status'.format(permission_prefix))
        config.add_tailbone_index_page(route_prefix, index_title,
                                       '{}.status'.format(permission_prefix))

        # restart
        config.add_tailbone_permission(permission_prefix,
                                       '{}.restart'.format(permission_prefix),
                                       label="Restart the DataSync daemon")
        config.add_route('{}.restart'.format(route_prefix),
                         '{}/restart'.format(url_prefix),
                         request_method='POST')
        config.add_view(cls, attr='restart',
                        route_name='{}.restart'.format(route_prefix),
                        permission='{}.restart'.format(permission_prefix))


class DataSyncChangeView(MasterView):
    """
    Master view for the DataSyncChange model.
    """
    model_class = model.DataSyncChange
    url_prefix = '/datasync/changes'
    permission_prefix = 'datasync_changes'
    creatable = False
    bulk_deletable = True

    labels = {
        'batch_id': "Batch ID",
    }

    grid_columns = [
        'source',
        'batch_id',
        'batch_sequence',
        'payload_type',
        'payload_key',
        'deletion',
        'obtained',
        'consumer',
    ]

    def configure_grid(self, g):
        super(DataSyncChangeView, self).configure_grid(g)

        # batch_sequence
        g.set_label('batch_sequence', "Batch Seq.")
        g.filters['batch_sequence'].label = "Batch Sequence"

        g.set_sort_defaults('obtained')
        g.set_type('obtained', 'datetime')

    def template_kwargs_index(self, **kwargs):
        kwargs['allow_filemon_restart'] = bool(self.rattail_config.get('tailbone', 'filemon.restart'))
        return kwargs

    def configure_form(self, f):
        super(DataSyncChangeView, self).configure_form(f)

        f.set_readonly('obtained')


# TODO: deprecate / remove this
DataSyncChangesView = DataSyncChangeView


def defaults(config, **kwargs):
    base = globals()
    rattail_config = config.registry['rattail_config']

    DataSyncThreadView = kwargs.get('DataSyncThreadView', base['DataSyncThreadView'])
    DataSyncThreadView.defaults(config)

    DataSyncChangeView = kwargs.get('DataSyncChangeView', base['DataSyncChangeView'])
    DataSyncChangeView.defaults(config)

    if should_expose_websockets(rattail_config):
        config.include('tailbone.views.asgi.datasync')


def includeme(config):
    defaults(config)
