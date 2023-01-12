# -*- coding: utf-8 -*-
"""add more newproduct batch row attrs

Revision ID: a20208a41889
Revises: 3b70d683b0cf
Create Date: 2022-08-30 13:44:05.579769

"""

from __future__ import unicode_literals, absolute_import

# revision identifiers, used by Alembic.
revision = 'a20208a41889'
down_revision = '3b70d683b0cf'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # batch_newproduct_row
    op.add_column('batch_newproduct_row', sa.Column('weighed', sa.Boolean(), nullable=True))
    op.add_column('batch_newproduct_row', sa.Column('tax1', sa.Boolean(), nullable=True))
    op.add_column('batch_newproduct_row', sa.Column('tax2', sa.Boolean(), nullable=True))
    op.add_column('batch_newproduct_row', sa.Column('tax3', sa.Boolean(), nullable=True))
    op.add_column('batch_newproduct_row', sa.Column('ecommerce_available', sa.Boolean(), nullable=True))


def downgrade():

    # batch_newproduct_row
    op.drop_column('batch_newproduct_row', 'ecommerce_available')
    op.drop_column('batch_newproduct_row', 'tax3')
    op.drop_column('batch_newproduct_row', 'tax2')
    op.drop_column('batch_newproduct_row', 'tax1')
    op.drop_column('batch_newproduct_row', 'weighed')
