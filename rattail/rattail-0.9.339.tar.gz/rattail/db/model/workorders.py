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
Data Models for Work Orders
"""

from __future__ import unicode_literals, absolute_import

import sqlalchemy as sa
from sqlalchemy import orm

from rattail.db.model import Base, uuid_column
from rattail.time import make_utc


class WorkOrder(Base):
    """
    Represents a generic work order for a customer.
    """
    __tablename__ = 'workorder'
    __table_args__ = (
        sa.ForeignKeyConstraint(['customer_uuid'], ['customer.uuid'], 
                                name='workorder_fk_customer'),
    )

    uuid = uuid_column()

    id = sa.Column(sa.Integer(), nullable=False, doc="""
    Numeric ID for the work order.
    """)

    customer_uuid = sa.Column(sa.String(length=32), nullable=False)
    customer = orm.relationship(
        'Customer',
        doc="""
        Reference to the customer who requested the work.
        """,
        backref=orm.backref(
            'workorders',
            doc="""
            Sequence of all work orders for this customer.
            """))

    estimated_total = sa.Column(sa.Numeric(precision=9, scale=2), nullable=True, doc="""
    Estimated total price to be charged to the customer, should the
    work order be fulfilled.
    """)

    date_submitted = sa.Column(sa.Date(), nullable=True, doc="""
    Date on which the work order was first "submitted" by the customer.
    """)

    date_received = sa.Column(sa.Date(), nullable=True, doc="""
    Date on which the org received the work order from the customer.
    """)

    date_released = sa.Column(sa.Date(), nullable=True, doc="""
    Date on which the org "released" (e.g. mailed) the work result
    back to the customer.
    """)

    date_delivered = sa.Column(sa.Date(), nullable=True, doc="""
    Date on which the work result was truly delivered back to the
    customer.
    """)

    notes = sa.Column(sa.Text(), nullable=True, doc="""
    Extra notes about the work order.
    """)

    status_code = sa.Column(sa.Integer(), nullable=False, doc="""
    Status code for the work order.
    """)

    status_text = sa.Column(sa.String(length=255), nullable=True, doc="""
    Text which may briefly explain the status code, if needed.
    """)

    def __str__(self):
        return "#{} for {}".format(self.id, self.customer)

    @property
    def id_str(self):
        if not self.id:
            return ''

        from rattail.batch import batch_id_str
        return batch_id_str(self.id)


class WorkOrderEvent(Base):
    """
    An event in the life of a work order
    """
    __tablename__ = 'workorder_event'
    __table_args__ = (
        sa.ForeignKeyConstraint(['workorder_uuid'], ['workorder.uuid'],
                                name='workorder_event_fk_workorder'),
        sa.ForeignKeyConstraint(['user_uuid'], ['user.uuid'],
                                name='workorder_event_fk_user'),
    )

    uuid = uuid_column()

    workorder_uuid = sa.Column(sa.String(length=32), nullable=False)
    workorder = orm.relationship(
        WorkOrder,
        doc="""
        Reference to the :class:`CustomerOrder` instance to which the item belongs.
        """,
        backref=orm.backref(
            'events',
            order_by='WorkOrderEvent.occurred',
            cascade='all, delete-orphan'))

    type_code = sa.Column(sa.Integer, nullable=False, doc="""
    Code specifying the type of event this is.
    """)

    occurred = sa.Column(sa.DateTime(), nullable=False, default=make_utc, doc="""
    Date and time when the event occurred.
    """)

    user_uuid = sa.Column(sa.String(length=32), nullable=False)
    user = orm.relationship(
        'User',
        doc="""
        User who was the "actor" for the event.
        """)

    note = sa.Column(sa.Text(), nullable=True, doc="""
    Optional note recorded for the event.
    """)
