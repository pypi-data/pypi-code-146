# -*- coding: utf-8 -*-
"""empty message

Revision ID: roc_dingo_0008_remove_date
Revises: roc_dingo_0007_add_error_log
Create Date: 2021-02-04 16:17:41.195180

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'roc_dingo_0008_remove_date'
down_revision = 'roc_dingo_0007_add_error_log'
branch_labels = None
depends_on = None


def upgrade():
    # Column date is useless.
    # All the information is in start/end time`
    # date column is irrelevant for monthly files.
    op.drop_column('file_log', 'date', schema='pipeline')


def downgrade():
    #
    op.add_column(
        'file_log',
        sa.Column('date', sa.DATE(), nullable=True),
        schema='pipeline')
