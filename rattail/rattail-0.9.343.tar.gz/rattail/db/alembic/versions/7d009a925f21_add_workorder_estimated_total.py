# -*- coding: utf-8; -*-
"""add workorder.estimated_total

Revision ID: 7d009a925f21
Revises: a20208a41889
Create Date: 2022-08-30 21:00:34.351167

"""

from __future__ import unicode_literals, absolute_import

# revision identifiers, used by Alembic.
revision = '7d009a925f21'
down_revision = 'a20208a41889'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # workorder
    op.add_column('workorder', sa.Column('estimated_total', sa.Numeric(precision=9, scale=2), nullable=True))


def downgrade():

    # workorder
    op.drop_column('workorder', 'estimated_total')
