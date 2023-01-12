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
Work Order Views
"""

from __future__ import unicode_literals, absolute_import

import sqlalchemy as sa

from rattail.db.model import WorkOrder, WorkOrderEvent

from webhelpers2.html import HTML

from tailbone import forms, grids
from tailbone.views import MasterView


class WorkOrderView(MasterView):
    """
    Master view for work orders
    """
    model_class = WorkOrder
    route_prefix = 'workorders'
    url_prefix = '/workorders'
    bulk_deletable = True

    labels = {
        'id': "ID",
        'status_code': "Status",
    }

    grid_columns = [
        'id',
        'customer',
        'date_received',
        'date_released',
        'status_code',
    ]

    form_fields = [
        'id',
        'customer',
        'notes',
        'date_submitted',
        'date_received',
        'date_released',
        'date_delivered',
        'status_code',
    ]

    has_rows = True
    model_row_class = WorkOrderEvent
    rows_viewable = False

    row_labels = {
        'type_code': "Event Type",
    }

    row_grid_columns = [
        'type_code',
        'occurred',
        'user',
        'note',
    ]

    def __init__(self, request):
        super(WorkOrderView, self).__init__(request)
        app = self.get_rattail_app()
        self.workorder_handler = app.get_workorder_handler()

    def configure_grid(self, g):
        super(WorkOrderView, self).configure_grid(g)
        model = self.model

        # customer
        g.set_joiner('customer', lambda q: q.join(model.Customer))
        g.set_sorter('customer', model.Customer.name)
        g.set_filter('customer', model.Customer.name)

        # status
        g.set_filter('status_code', model.WorkOrder.status_code,
                     factory=StatusFilter,
                     default_active=True,
                     default_verb='is_active')
        g.set_enum('status_code', self.enum.WORKORDER_STATUS)

        g.set_sort_defaults('id', 'desc')

        g.set_link('id')
        g.set_link('customer')

    def grid_extra_class(self, workorder, i):
        if workorder.status_code == self.enum.WORKORDER_STATUS_CANCELED:
            return 'warning'

    def configure_form(self, f):
        super(WorkOrderView, self).configure_form(f)
        model = self.model
        use_buefy = self.get_use_buefy()
        SelectWidget = forms.widgets.JQuerySelectWidget

        # id
        if self.creating:
            f.remove_field('id')
        else:
            f.set_readonly('id')

        # customer
        if self.creating:
            f.replace('customer', 'customer_uuid')
            f.set_label('customer_uuid', "Customer")
            f.set_widget('customer_uuid',
                         forms.widgets.make_customer_widget(self.request))
            f.set_input_handler('customer_uuid', 'customerChanged')
        else:
            f.set_readonly('customer')
            f.set_renderer('customer', self.render_customer)

        # notes
        f.set_type('notes', 'text')

        # status_code
        if self.creating:
            f.remove('status_code')
        else:
            f.set_enum('status_code', self.enum.WORKORDER_STATUS)
            f.set_renderer('status_code', self.render_status_code)
            if not self.has_perm('edit_status'):
                f.set_readonly('status_code')

        # date fields
        f.set_type('date_submitted', 'date_jquery')
        f.set_type('date_received', 'date_jquery')
        f.set_type('date_released', 'date_jquery')
        f.set_type('date_delivered', 'date_jquery')
        if self.creating:
            f.remove('date_submitted',
                     'date_received',
                     'date_released',
                     'date_delivered')
        elif not self.has_perm('edit_status'):
            f.set_readonly('date_submitted')
            f.set_readonly('date_received')
            f.set_readonly('date_released')
            f.set_readonly('date_delivered')

    def objectify(self, form, data=None):
        """
        Supplements the default logic as follows:

        If creating a new Work Order, will automatically set its status to
        "submitted" and its ``date_submitted`` to the current date.
        """
        if data is None:
            data = form.validated

        # first let deform do its thing.  if editing, this will update
        # the record like we want.  but if creating, this will
        # populate the initial object *without* adding it to session,
        # which is also what we want, so that we can "replace" the new
        # object with one the handler creates, below
        workorder = form.schema.objectify(data, context=form.model_instance)

        if self.creating:

            # now make the "real" work order
            data = dict([(key, getattr(workorder, key))
                         for key in data])
            workorder = self.workorder_handler.make_workorder(self.Session(), **data)

        return workorder

    def render_status_code(self, obj, field):
        status_code = getattr(obj, field)
        if status_code is None:
            return ""
        if status_code in self.enum.WORKORDER_STATUS:
            text = self.enum.WORKORDER_STATUS[status_code]
            if status_code == self.enum.WORKORDER_STATUS_CANCELED:
                use_buefy = self.get_use_buefy()
                if use_buefy:
                    return HTML.tag('span', class_='has-text-danger', c=text)
                else:
                    return HTML.tag('span', style='color: red;', c=text)
            return text
        return str(status_code)

    def get_row_data(self, workorder):
        model = self.model
        return self.Session.query(model.WorkOrderEvent)\
                           .filter(model.WorkOrderEvent.workorder == workorder)

    def get_parent(self, event):
        return event.workorder

    def configure_row_grid(self, g):
        super(WorkOrderView, self).configure_row_grid(g)
        g.set_enum('type_code', self.enum.WORKORDER_EVENT)
        g.set_sort_defaults('occurred')

    def receive(self):
        """
        Sets work order status to "received".
        """
        workorder = self.get_instance()
        self.workorder_handler.receive(workorder)
        self.Session.flush()
        return self.redirect(self.get_action_url('view', workorder))

    def await_estimate(self):
        """
        Sets work order status to "awaiting estimate confirmation".
        """
        workorder = self.get_instance()
        self.workorder_handler.await_estimate(workorder)
        self.Session.flush()
        return self.redirect(self.get_action_url('view', workorder))

    def await_parts(self):
        """
        Sets work order status to "awaiting parts".
        """
        workorder = self.get_instance()
        self.workorder_handler.await_parts(workorder)
        self.Session.flush()
        return self.redirect(self.get_action_url('view', workorder))

    def work_on_it(self):
        """
        Sets work order status to "working on it".
        """
        workorder = self.get_instance()
        self.workorder_handler.work_on_it(workorder)
        self.Session.flush()
        return self.redirect(self.get_action_url('view', workorder))

    def release(self):
        """
        Sets work order status to "released".
        """
        workorder = self.get_instance()
        self.workorder_handler.release(workorder)
        self.Session.flush()
        return self.redirect(self.get_action_url('view', workorder))

    def deliver(self):
        """
        Sets work order status to "delivered".
        """
        workorder = self.get_instance()
        self.workorder_handler.deliver(workorder)
        self.Session.flush()
        return self.redirect(self.get_action_url('view', workorder))

    def cancel(self):
        """
        Sets work order status to "canceled".
        """
        workorder = self.get_instance()
        self.workorder_handler.cancel(workorder)
        self.Session.flush()
        return self.redirect(self.get_action_url('view', workorder))

    @classmethod
    def defaults(cls, config):
        cls._defaults(config)
        cls._workorder_defaults(config)

    @classmethod
    def _workorder_defaults(cls, config):
        route_prefix = cls.get_route_prefix()
        permission_prefix = cls.get_permission_prefix()
        instance_url_prefix = cls.get_instance_url_prefix()
        model_title = cls.get_model_title()

        # perm for editing status
        config.add_tailbone_permission(
            permission_prefix,
            '{}.edit_status'.format(permission_prefix),
            "Directly edit status and related fields for {}".format(model_title))

        # receive
        config.add_route('{}.receive'.format(route_prefix),
                         '{}/receive'.format(instance_url_prefix),
                         request_method='POST')
        config.add_view(cls, attr='receive',
                        route_name='{}.receive'.format(route_prefix),
                        permission='{}.edit'.format(permission_prefix))

        # await_estimate
        config.add_route('{}.await_estimate'.format(route_prefix),
                         '{}/await-estimate'.format(instance_url_prefix),
                         request_method='POST')
        config.add_view(cls, attr='await_estimate',
                        route_name='{}.await_estimate'.format(route_prefix),
                        permission='{}.edit'.format(permission_prefix))

        # await_parts
        config.add_route('{}.await_parts'.format(route_prefix),
                         '{}/await-parts'.format(instance_url_prefix),
                         request_method='POST')
        config.add_view(cls, attr='await_parts',
                        route_name='{}.await_parts'.format(route_prefix),
                        permission='{}.edit'.format(permission_prefix))

        # work_on_it
        config.add_route('{}.work_on_it'.format(route_prefix),
                         '{}/work-on-it'.format(instance_url_prefix),
                         request_method='POST')
        config.add_view(cls, attr='work_on_it',
                        route_name='{}.work_on_it'.format(route_prefix),
                        permission='{}.edit'.format(permission_prefix))

        # release
        config.add_route('{}.release'.format(route_prefix),
                         '{}/release'.format(instance_url_prefix),
                         request_method='POST')
        config.add_view(cls, attr='release',
                        route_name='{}.release'.format(route_prefix),
                        permission='{}.edit'.format(permission_prefix))

        # deliver
        config.add_route('{}.deliver'.format(route_prefix),
                         '{}/deliver'.format(instance_url_prefix),
                         request_method='POST')
        config.add_view(cls, attr='deliver',
                        route_name='{}.deliver'.format(route_prefix),
                        permission='{}.edit'.format(permission_prefix))

        # cancel
        config.add_route('{}.cancel'.format(route_prefix),
                         '{}/cancel'.format(instance_url_prefix),
                         request_method='POST')
        config.add_view(cls, attr='cancel',
                        route_name='{}.cancel'.format(route_prefix),
                        permission='{}.edit'.format(permission_prefix))


class StatusFilter(grids.filters.AlchemyIntegerFilter):

    def __init__(self, *args, **kwargs):
        super(StatusFilter, self).__init__(*args, **kwargs)

        from drild import enum

        self.active_status_codes = [
            # enum.WORKORDER_STATUS_CREATED,
            enum.WORKORDER_STATUS_SUBMITTED,
            enum.WORKORDER_STATUS_RECEIVED,
            enum.WORKORDER_STATUS_PENDING_ESTIMATE,
            enum.WORKORDER_STATUS_WAITING_FOR_PARTS,
            enum.WORKORDER_STATUS_WORKING_ON_IT,
            enum.WORKORDER_STATUS_RELEASED,
        ]

    @property
    def verb_labels(self):
        labels = dict(super(StatusFilter, self).verb_labels)
        labels['is_active'] = "Is Active"
        labels['not_active'] = "Is Not Active"
        return labels

    @property
    def valueless_verbs(self):
        verbs = list(super(StatusFilter, self).valueless_verbs)
        verbs.extend([
            'is_active',
            'not_active',
        ])
        return verbs

    @property
    def default_verbs(self):
        verbs = list(super(StatusFilter, self).default_verbs)
        verbs.insert(0, 'is_active')
        verbs.insert(1, 'not_active')
        return verbs

    def filter_is_active(self, query, value):
        return query.filter(
            WorkOrder.status_code.in_(self.active_status_codes))

    def filter_not_active(self, query, value):
        return query.filter(sa.or_(
            ~WorkOrder.status_code.in_(self.active_status_codes),
            WorkOrder.status_code == None,
        ))


def defaults(config, **kwargs):
    base = globals()

    WorkOrderView = kwargs.get('WorkOrderView', base['WorkOrderView'])
    WorkOrderView.defaults(config)


def includeme(config):
    defaults(config)
