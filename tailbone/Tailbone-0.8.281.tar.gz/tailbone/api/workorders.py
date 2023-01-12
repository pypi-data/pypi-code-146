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
Tailbone Web API - Work Order Views
"""

from __future__ import unicode_literals, absolute_import

import datetime

import six

from rattail.db.model import WorkOrder

from cornice import Service

from tailbone.api import APIMasterView


class WorkOrderView(APIMasterView):

    model_class = WorkOrder
    collection_url_prefix = '/workorders'
    object_url_prefix = '/workorder'

    def __init__(self, *args, **kwargs):
        super(WorkOrderView, self).__init__(*args, **kwargs)
        app = self.get_rattail_app()
        self.workorder_handler = app.get_workorder_handler()

    def normalize(self, workorder):
        data = super(WorkOrderView, self).normalize(workorder)
        data.update({
            'customer_name': workorder.customer.name,
            'status_label': self.enum.WORKORDER_STATUS[workorder.status_code],
            'date_submitted': six.text_type(workorder.date_submitted or ''),
            'date_received': six.text_type(workorder.date_received or ''),
            'date_released': six.text_type(workorder.date_released or ''),
            'date_delivered': six.text_type(workorder.date_delivered or ''),
        })
        return data

    def create_object(self, data):

        # invoke the handler instead of normal API CRUD logic
        workorder = self.workorder_handler.make_workorder(self.Session(), **data)
        return workorder

    def update_object(self, workorder, data):
        date_fields = [
            'date_submitted',
            'date_received',
            'date_released',
            'date_delivered',
        ]

        # coerce date field values to proper datetime.date objects
        for field in date_fields:
            if field in data:
                if data[field] == '':
                    data[field] = None
                elif not isinstance(data[field], datetime.date):
                    date = datetime.datetime.strptime(data[field], '%Y-%m-%d').date()
                    data[field] = date

        # coerce status code value to proper integer
        if 'status_code' in data:
            data['status_code'] = int(data['status_code'])

        return super(WorkOrderView, self).update_object(workorder, data)

    def status_codes(self):
        """
        Retrieve all info about possible work order status codes.
        """
        return self.workorder_handler.status_codes()

    def receive(self):
        """
        Sets work order status to "received".
        """
        workorder = self.get_object()
        self.workorder_handler.receive(workorder)
        self.Session.flush()
        return self.normalize(workorder)

    def await_estimate(self):
        """
        Sets work order status to "awaiting estimate confirmation".
        """
        workorder = self.get_object()
        self.workorder_handler.await_estimate(workorder)
        self.Session.flush()
        return self.normalize(workorder)

    def await_parts(self):
        """
        Sets work order status to "awaiting parts".
        """
        workorder = self.get_object()
        self.workorder_handler.await_parts(workorder)
        self.Session.flush()
        return self.normalize(workorder)

    def work_on_it(self):
        """
        Sets work order status to "working on it".
        """
        workorder = self.get_object()
        self.workorder_handler.work_on_it(workorder)
        self.Session.flush()
        return self.normalize(workorder)

    def release(self):
        """
        Sets work order status to "released".
        """
        workorder = self.get_object()
        self.workorder_handler.release(workorder)
        self.Session.flush()
        return self.normalize(workorder)

    def deliver(self):
        """
        Sets work order status to "delivered".
        """
        workorder = self.get_object()
        self.workorder_handler.deliver(workorder)
        self.Session.flush()
        return self.normalize(workorder)

    def cancel(self):
        """
        Sets work order status to "canceled".
        """
        workorder = self.get_object()
        self.workorder_handler.cancel(workorder)
        self.Session.flush()
        return self.normalize(workorder)

    @classmethod
    def defaults(cls, config):
        cls._defaults(config)
        cls._workorder_defaults(config)

    @classmethod
    def _workorder_defaults(cls, config):
        route_prefix = cls.get_route_prefix()
        permission_prefix = cls.get_permission_prefix()
        collection_url_prefix = cls.get_collection_url_prefix()
        object_url_prefix = cls.get_object_url_prefix()

        # status codes
        status_codes = Service(name='{}.status_codes'.format(route_prefix),
                               path='{}/status-codes'.format(collection_url_prefix))
        status_codes.add_view('GET', 'status_codes', klass=cls,
                              permission='{}.list'.format(permission_prefix))
        config.add_cornice_service(status_codes)

        # receive
        receive = Service(name='{}.receive'.format(route_prefix),
                          path='{}/{{uuid}}/receive'.format(object_url_prefix))
        receive.add_view('POST', 'receive', klass=cls,
                         permission='{}.edit'.format(permission_prefix))
        config.add_cornice_service(receive)

        # await estimate confirmation
        await_estimate = Service(name='{}.await_estimate'.format(route_prefix),
                                 path='{}/{{uuid}}/await-estimate'.format(object_url_prefix))
        await_estimate.add_view('POST', 'await_estimate', klass=cls,
                                permission='{}.edit'.format(permission_prefix))
        config.add_cornice_service(await_estimate)

        # await parts
        await_parts = Service(name='{}.await_parts'.format(route_prefix),
                              path='{}/{{uuid}}/await-parts'.format(object_url_prefix))
        await_parts.add_view('POST', 'await_parts', klass=cls,
                             permission='{}.edit'.format(permission_prefix))
        config.add_cornice_service(await_parts)

        # work on it
        work_on_it = Service(name='{}.work_on_it'.format(route_prefix),
                             path='{}/{{uuid}}/work-on-it'.format(object_url_prefix))
        work_on_it.add_view('POST', 'work_on_it', klass=cls,
                            permission='{}.edit'.format(permission_prefix))
        config.add_cornice_service(work_on_it)

        # release
        release = Service(name='{}.release'.format(route_prefix),
                          path='{}/{{uuid}}/release'.format(object_url_prefix))
        release.add_view('POST', 'release', klass=cls,
                         permission='{}.edit'.format(permission_prefix))
        config.add_cornice_service(release)

        # deliver
        deliver = Service(name='{}.deliver'.format(route_prefix),
                          path='{}/{{uuid}}/deliver'.format(object_url_prefix))
        deliver.add_view('POST', 'deliver', klass=cls,
                         permission='{}.edit'.format(permission_prefix))
        config.add_cornice_service(deliver)

        # cancel
        cancel = Service(name='{}.cancel'.format(route_prefix),
                         path='{}/{{uuid}}/cancel'.format(object_url_prefix))
        cancel.add_view('POST', 'cancel', klass=cls,
                        permission='{}.edit'.format(permission_prefix))
        config.add_cornice_service(cancel)


def defaults(config, **kwargs):
    base = globals()

    WorkOrderView = kwargs.get('WorkOrderView', base['WorkOrderView'])
    WorkOrderView.defaults(config)


def includeme(config):
    defaults(config)
