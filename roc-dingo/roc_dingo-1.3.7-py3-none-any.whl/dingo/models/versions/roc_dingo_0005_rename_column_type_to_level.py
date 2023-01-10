# -*- coding: utf-8 -*-
"""Rename column type to level

Revision ID: 0005
Revises: roc_dingo_0004_modify_file_log
Create Date: 2020-10-14 14:37:49.295678

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'roc_dingo_0005_mv_type_level'
down_revision = 'roc_dingo_0004_modify_file_log'
depends_on = None


def upgrade():
    op.execute('DROP TYPE IF EXISTS file_level_list')
    op.execute('ALTER TYPE file_type_list  RENAME TO file_level_list')

    # rename type -> level
    op.alter_column(
        'file_log', 'type',
        new_column_name='level', schema='pipeline')


def downgrade():

    op.execute('ALTER TYPE file_level_list RENAME TO file_type_list')

    # rename level -> type
    op.alter_column(
        'file_log', 'level',
        new_column_name='type', schema='pipeline')
