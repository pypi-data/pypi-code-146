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
Work Order Handler
"""

from __future__ import unicode_literals, absolute_import

from rattail.app import GenericHandler


class WorkOrderHandler(GenericHandler):
    """
    Handler for work orders.
    """

    def make_workorder(self, session, **kwargs):
        """
        Make and return a new work order.
        """
        model = self.model

        if 'id' not in kwargs:
            kwargs['id'] = self.app.next_counter_value(session, 'workorder_id')

        if 'date_submitted' not in kwargs:
            kwargs['date_submitted'] = self.app.today()

        if 'status_code' not in kwargs:
            kwargs['status_code'] = self.enum.WORKORDER_STATUS_SUBMITTED

        workorder = model.WorkOrder(**kwargs)
        session.add(workorder)
        self.record_event(workorder, self.enum.WORKORDER_EVENT_SUBMITTED)
        session.flush()
        return workorder

    def status_codes(self):
        """
        Retrieve all info about possible work order status codes.
        """
        code_names = {}
        for name in dir(self.enum):
            if name.startswith('WORKORDER_STATUS_'):
                code_names[getattr(self.enum, name)] = name

        status_codes = []
        for key, label in self.enum.WORKORDER_STATUS.items():
            status_codes.append({
                'code': key,
                'code_name': code_names[key],
                'label': label,
            })

        return status_codes

    def record_event(self, workorder, type_code, **kwargs):
        model = self.model

        # who did this?
        if 'user' in kwargs:
            user = kwargs['user']
        else:
            session = kwargs.get('session') or self.app.get_session(workorder)
            user = session.continuum_user
        kwargs['user'] = user

        # record the event
        workorder.events.append(model.WorkOrderEvent(
            type_code=type_code, **kwargs))

    def receive(self, workorder, **kwargs):
        """
        Sets work order status to "received".
        """
        workorder.status_code = self.enum.WORKORDER_STATUS_RECEIVED
        workorder.date_received = self.app.today()
        self.record_event(workorder, self.enum.WORKORDER_EVENT_RECEIVED)

    def await_estimate(self, workorder):
        """
        Sets work order status to "awaiting estimate confirmation".
        """
        workorder.status_code = self.enum.WORKORDER_STATUS_PENDING_ESTIMATE
        self.record_event(workorder, self.enum.WORKORDER_EVENT_PENDING_ESTIMATE)

    def await_parts(self, workorder):
        """
        Sets work order status to "awaiting parts".
        """
        workorder.status_code = self.enum.WORKORDER_STATUS_WAITING_FOR_PARTS
        self.record_event(workorder, self.enum.WORKORDER_EVENT_WAITING_FOR_PARTS)

    def work_on_it(self, workorder):
        """
        Sets work order status to "working on it".
        """
        workorder.status_code = self.enum.WORKORDER_STATUS_WORKING_ON_IT
        self.record_event(workorder, self.enum.WORKORDER_EVENT_WORKING_ON_IT)

    def release(self, workorder):
        """
        Sets work order status to "released".
        """
        workorder.status_code = self.enum.WORKORDER_STATUS_RELEASED
        workorder.date_released = self.app.today()
        self.record_event(workorder, self.enum.WORKORDER_EVENT_RELEASED)

    def deliver(self, workorder):
        """
        Sets work order status to "delivered".
        """
        workorder.status_code = self.enum.WORKORDER_STATUS_DELIVERED
        workorder.date_delivered = self.app.today()
        self.record_event(workorder, self.enum.WORKORDER_EVENT_DELIVERED)

    def cancel(self, workorder):
        """
        Sets work order status to "canceled".
        """
        workorder.status_code = self.enum.WORKORDER_STATUS_CANCELED
        self.record_event(workorder, self.enum.WORKORDER_EVENT_CANCELED)
