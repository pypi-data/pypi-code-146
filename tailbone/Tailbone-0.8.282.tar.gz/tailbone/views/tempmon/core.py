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
Common stuff for tempmon views
"""

from __future__ import unicode_literals, absolute_import

from webhelpers2.html import HTML

from tailbone import views, grids
from tailbone.db import TempmonSession


class MasterView(views.MasterView):
    """
    Base class for tempmon views.
    """
    Session = TempmonSession

    def get_bulk_delete_session(self):
        from rattail_tempmon.db import Session
        return Session()

    def normalize_probes(self, probes):
        data = []
        for probe in probes:
            view_url = self.request.route_url('tempmon.probes.view', uuid=probe.uuid)
            edit_url = self.request.route_url('tempmon.probes.edit', uuid=probe.uuid)
            data.append({
                'uuid': probe.uuid,
                'url': view_url,
                '_action_url_view': view_url,
                '_action_url_edit': edit_url,
                'description': probe.description,
                'critical_temp_min': probe.critical_temp_min,
                'good_temp_min': probe.good_temp_min,
                'good_temp_max': probe.good_temp_max,
                'critical_temp_max': probe.critical_temp_max,
                'status': self.enum.TEMPMON_PROBE_STATUS[probe.status],
                'enabled': "Yes" if probe.enabled else "No",
            })
        app = self.get_rattail_app()
        data = app.json_friendly(data)
        return data

    def render_probes(self, obj, field):
        """
        This method is used by Appliance and Client views.
        """
        if not obj.probes:
            return ""

        route_prefix = self.get_route_prefix()
        use_buefy = self.get_use_buefy()
        if use_buefy:

            actions = [self.make_grid_action_view()]
            if self.request.has_perm('tempmon.probes.edit'):
                actions.append(self.make_grid_action_edit())

            factory = self.get_grid_factory()
            g = factory(
                key='{}.probes'.format(route_prefix),
                data=[],
                columns=[
                    'description',
                    'critical_temp_min',
                    'good_temp_min',
                    'good_temp_max',
                    'critical_temp_max',
                    'status',
                    'enabled',
                ],
                labels={
                    'critical_temp_min': "Crit. Min",
                    'good_temp_min': "Good Min",
                    'good_temp_max': "Good Max",
                    'critical_temp_max': "Crit. Max",
                },
                linked_columns=['description'],
                main_actions=actions,
            )
            return HTML.literal(
                g.render_buefy_table_element(data_prop='probesData'))

        # not buefy!
        view_url = lambda p, i: self.request.route_url('tempmon.probes.view', uuid=p.uuid)
        actions = [
            grids.GridAction('view', icon='zoomin', url=view_url),
        ]
        if self.request.has_perm('tempmon.probes.edit'):
            url = lambda p, i: self.request.route_url('tempmon.probes.edit', uuid=p.uuid)
            actions.append(grids.GridAction('edit', icon='pencil', url=url))

        g = grids.Grid(
            key='{}.probes'.format(route_prefix),
            data=obj.probes,
            columns=[
                'description',
                'critical_temp_min',
                'good_temp_min',
                'good_temp_max',
                'critical_temp_max',
                'status',
                'enabled',
            ],
            labels={
                'critical_temp_min': "Crit. Min",
                'good_temp_min': "Good Min",
                'good_temp_max': "Good Max",
                'critical_temp_max': "Crit. Max",
            },
            url=lambda p: self.request.route_url('tempmon.probes.view', uuid=p.uuid),
            linked_columns=['description'],
            main_actions=actions,
        )
        g.set_enum('status', self.enum.TEMPMON_PROBE_STATUS)
        g.set_type('enabled', 'boolean')
        return HTML.literal(g.render_grid())
