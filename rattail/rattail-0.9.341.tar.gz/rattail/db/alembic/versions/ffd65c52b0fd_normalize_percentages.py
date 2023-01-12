# -*- coding: utf-8; -*-
"""normalize percentages

Revision ID: ffd65c52b0fd
Revises: 7d009a925f21
Create Date: 2022-10-29 13:06:49.034231

"""

from __future__ import unicode_literals, absolute_import

# revision identifiers, used by Alembic.
revision = 'ffd65c52b0fd'
down_revision = '7d009a925f21'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types


product_volatile = sa.sql.table('product_volatile',
                                sa.sql.column('true_margin'))


def convert_all(convert):

    # product_volatile
    op.execute(product_volatile.update()\
               .where(product_volatile.c.true_margin != None)\
               .values({'true_margin': convert(product_volatile.c.true_margin)}))


def upgrade():

    # product_volatile
    op.alter_column('product_volatile', 'true_margin', type_=sa.Numeric(precision=9, scale=5))

    # batch_pricing_row
    op.alter_column('batch_pricing_row', 'old_true_margin', type_=sa.Numeric(precision=9, scale=5))
    op.alter_column('batch_pricing_row', 'true_margin', type_=sa.Numeric(precision=9, scale=5))

    # input values are 0.0 - 1.0 range, output is 0 - 100
    convert_all(lambda val: val * 100)


def downgrade():

    # input values are 0 - 100 range, output is 0.0 - 1.0
    convert_all(lambda val: val / 100.0)

    # batch_pricing_row
    op.alter_column('batch_pricing_row', 'old_true_margin', type_=sa.Numeric(precision=8, scale=3))
    op.alter_column('batch_pricing_row', 'true_margin', type_=sa.Numeric(precision=8, scale=3))

    # product_volatile
    op.alter_column('product_volatile', 'true_margin', type_=sa.Numeric(precision=8, scale=5))
