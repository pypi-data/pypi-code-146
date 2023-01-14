# -*- coding: utf-8 -*-
"""add more newproduct batch row attrs

Revision ID: 3b70d683b0cf
Revises: d39ff41238fa
Create Date: 2022-08-30 09:29:38.260962

"""

from __future__ import unicode_literals, absolute_import

# revision identifiers, used by Alembic.
revision = '3b70d683b0cf'
down_revision = 'd39ff41238fa'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # batch_newproduct_row
    op.add_column('batch_newproduct_row', sa.Column('unit_size', sa.Numeric(precision=8, scale=3), nullable=True))
    op.add_column('batch_newproduct_row', sa.Column('unit_of_measure', sa.String(length=4), nullable=True))
    op.add_column('batch_newproduct_row', sa.Column('unit_of_measure_entry', sa.String(length=20), nullable=True))


def downgrade():

    # batch_newproduct_row
    op.drop_column('batch_newproduct_row', 'unit_of_measure_entry')
    op.drop_column('batch_newproduct_row', 'unit_of_measure')
    op.drop_column('batch_newproduct_row', 'unit_size')
