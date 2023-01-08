# -*- coding: utf-8; -*-
"""add vendor terms

Revision ID: 90e3b9ea5356
Revises: dc28b97c33ff
Create Date: 2022-12-21 17:33:48.900595

"""

from __future__ import unicode_literals, absolute_import

# revision identifiers, used by Alembic.
revision = '90e3b9ea5356'
down_revision = 'dc28b97c33ff'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # vendor
    op.add_column('vendor', sa.Column('terms', sa.String(length=100), nullable=True))
    op.add_column('vendor_version', sa.Column('terms', sa.String(length=100), autoincrement=False, nullable=True))


def downgrade():

    # vendor
    op.drop_column('vendor_version', 'terms')
    op.drop_column('vendor', 'terms')
