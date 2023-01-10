# -*- coding: utf-8 -*-
"""empty message

Revision ID: roc_dingo_0009_add_bia
Revises: roc_dingo_0008_remove_date
Create Date: 2021-02-09 14:48:04.289978

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'roc_dingo_0009_add_bia'
down_revision = 'roc_dingo_0008_remove_date'
branch_labels = None
depends_on = None


def upgrade():
    # ADD BIA in the levels

    op.execute('COMMIT')
    op.execute("ALTER TYPE file_level_list ADD VALUE IF NOT EXISTS 'BIA'")


def downgrade():

    # Postgresl does not offer the ability to remove a value from an
    # enumerate type

    pass
