# -*- coding: utf-8; -*-
"""remove unique constraint for brand name

Revision ID: 0848a1761233
Revises: 62cfde95d655
Create Date: 2022-08-12 19:32:16.365448

"""

from __future__ import unicode_literals, absolute_import

# revision identifiers, used by Alembic.
revision = '0848a1761233'
down_revision = u'62cfde95d655'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # brand
    op.drop_constraint(u'brand_uq_name', 'brand', type_='unique')


def downgrade():

    # brand
    op.create_unique_constraint(u'brand_uq_name', 'brand', ['name'])
