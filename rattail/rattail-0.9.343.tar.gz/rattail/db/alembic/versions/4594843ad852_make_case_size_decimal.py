# -*- coding: utf-8; -*-
"""make case_size decimal

Revision ID: 4594843ad852
Revises: 90e3b9ea5356
Create Date: 2022-12-22 16:14:36.139342

"""

from __future__ import unicode_literals, absolute_import

# revision identifiers, used by Alembic.
revision = '4594843ad852'
down_revision = '90e3b9ea5356'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # batch_vendorcatalog_row
    op.alter_column('batch_vendorcatalog_row', 'case_size', type_=sa.Numeric(precision=9, scale=4))
    op.alter_column('batch_vendorcatalog_row', 'old_case_size', type_=sa.Numeric(precision=9, scale=4))

    # batch_vendorinvoice_row
    op.alter_column('batch_vendorinvoice_row', 'case_quantity', type_=sa.Numeric(precision=9, scale=4))


def downgrade():

    # batch_vendorinvoice_row
    op.alter_column('batch_vendorinvoice_row', 'case_quantity', type_=sa.Integer())

    # batch_vendorcatalog_row
    op.alter_column('batch_vendorcatalog_row', 'case_size', type_=sa.Integer())
    op.alter_column('batch_vendorcatalog_row', 'old_case_size', type_=sa.Integer())
