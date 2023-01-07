# -*- coding: utf-8; -*-
"""normalize catalog percents

Revision ID: dc28b97c33ff
Revises: ffd65c52b0fd
Create Date: 2022-11-28 11:31:21.447456

"""

from __future__ import unicode_literals, absolute_import

# revision identifiers, used by Alembic.
revision = 'dc28b97c33ff'
down_revision = 'ffd65c52b0fd'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types


batch_vendorcatalog_row = sa.sql.table('batch_vendorcatalog_row',
                                       sa.sql.column('unit_cost_diff_percent'),
                                       sa.sql.column('discount_percent'))


def convert_all(convert):

    # batch_vendorcatalog_row
    op.execute(batch_vendorcatalog_row.update()\
               .where(batch_vendorcatalog_row.c.unit_cost_diff_percent != None)\
               .values({'unit_cost_diff_percent': convert(batch_vendorcatalog_row.c.unit_cost_diff_percent)}))
    op.execute(batch_vendorcatalog_row.update()\
               .where(batch_vendorcatalog_row.c.discount_percent != None)\
               .values({'discount_percent': convert(batch_vendorcatalog_row.c.discount_percent)}))


def upgrade():

    # input values are 0.0 - 1.0 range, output is 0 - 100
    convert_all(lambda val: val * 100)


def downgrade():

    # input values are 0 - 100 range, output is 0.0 - 1.0
    convert_all(lambda val: val / 100.0)
