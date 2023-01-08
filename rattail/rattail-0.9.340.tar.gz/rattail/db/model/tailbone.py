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
Data models for Tailbone
"""

from __future__ import unicode_literals, absolute_import

import six
import sqlalchemy as sa

from rattail.db.model import Base, uuid_column


@six.python_2_unicode_compatible
class TailbonePageHelp(Base):
    """
    Represents help info for a particular page (or more often, set of
    pages) within Tailbone.
    """
    __tablename__ = 'tailbone_page_help'
    __table_args__ = (
        sa.UniqueConstraint('route_prefix',
                            name='tailbone_page_help_uq_route_prefix'),
    )
    __versioned__ = {}

    uuid = uuid_column()

    route_prefix = sa.Column(sa.String(length=254), nullable=False, doc="""
    Route prefix in Tailbone, to which this help info applies.
    """)

    help_url = sa.Column(sa.String(length=254), nullable=True, doc="""
    URL to (probably external) help document.
    """)

    markdown_text = sa.Column(sa.Text(), nullable=True, doc="""
    Help text as markdown.
    """)

    def __str__(self):
        return self.route_prefix or ''


@six.python_2_unicode_compatible
class TailboneFieldInfo(Base):
    """
    Represents info for a particular form field within Tailbone.
    """
    __tablename__ = 'tailbone_field_info'
    __table_args__ = (
        sa.UniqueConstraint('route_prefix', 'field_name',
                            name='tailbone_field_info_uq_field'),
    )
    __versioned__ = {}

    uuid = uuid_column()

    route_prefix = sa.Column(sa.String(length=254), nullable=False, doc="""
    Route prefix in Tailbone, to which this help info applies.
    """)

    field_name = sa.Column(sa.String(length=100), nullable=False, doc="""
    Name of the field within Tailbone code.
    """)

    markdown_text = sa.Column(sa.Text(), nullable=True, doc="""
    Help text as markdown.
    """)

    def __str__(self):
        return self.route_prefix or ''
