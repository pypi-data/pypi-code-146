# -*- coding: utf-8 -*-
"""empty message

Revision ID: roc_dingo_0007_add_error_log
Revises: roc_dingo_0006_add_is_removed
Create Date: 2020-12-17 11:38:09.315512

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'roc_dingo_0007_add_error_log'
down_revision = 'roc_dingo_0006_add_is_removed'
branch_labels = None
depends_on = None


def upgrade():

    # ADD error_log column

    op.add_column(
        'file_log',
        sa.Column('error_log', sa.String(), nullable=True),
        schema='pipeline')

    # ADD SPICE_KERNEL in the levels

    op.execute('COMMIT')
    op.execute("ALTER TYPE file_level_list ADD VALUE IF NOT EXISTS 'SK'")


def downgrade():
    op.drop_column('file_log', 'error_log', schema='pipeline')

    # Postgresl does not offer the ability to remove a value from an
    # enumerate type
    # Sk is not removed from enumerate type
    # the 'IF EXISTS' option is set in upgrade() to allow
    # multiple succesive upgrade/downgrade
