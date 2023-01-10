# -*- coding: utf-8 -*-
"""
Add new column product that will receive name
without version and file extension

Revision ID: roc_dingo_0018_add_product_to_file_log
Revises: roc_dingo_0017_add_efecsevents
Create Date: 2021-11-29 16:11:25.270861

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'roc_dingo_0018b_add_product_to_file_log'
down_revision = 'roc_dingo_0018a_task_delivered'
branch_labels = None
depends_on = None


def upgrade():

    # Add the new column product
    op.add_column(
        'file_log',
        sa.Column('product', sa.String(length=512), nullable=True),
        schema='pipeline')

    # Fill it
    op.execute("""
        UPDATE pipeline.file_log
        SET product = regexp_replace(
            basename, '^([^\\.]+)_V[0-9U]+\\.[^$]+$', '\\1')
        """)

    # Set nullable=False after filling
    op.alter_column(
        'file_log', 'product',
        existing_type=sa.VARCHAR(),
        nullable=False,
        schema='pipeline')


def downgrade():

    op.drop_column('file_log', 'product', schema='pipeline')
