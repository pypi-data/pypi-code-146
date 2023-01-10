# -*- coding: utf-8 -*-
"""empty message

Revision ID: roc_dingo_0022_add_to_update_flag_to_filelog
Revises: roc_dingo_0021_add_retrieved_time
Create Date: 2022-01-11 16:07:33.943889

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'roc_dingo_0022_add_to_update_flag_to_filelog'
down_revision = 'roc_dingo_0021_add_retrieved_time'
branch_labels = None
depends_on = None


def upgrade():
    # Add "to_update" flag with a default value to false
    # Trick to set a default value to the non null column
    # https://gist.github.com/VladimirPal/e256d19df8d85234dde1
    # it avoids to create with nullable=true, set the colum to false and
    # then set nullable=false
    op.add_column('file_log',
                  sa.Column('to_update',
                            sa.BOOLEAN(),
                            server_default=sa.schema.DefaultClause('0'),
                            nullable=False),
                  schema='pipeline')

    # Ensure is_removed and is_delivered are set to False

    op.alter_column('file_log', 'is_archived',
                    server_default=sa.schema.DefaultClause('0'),
                    schema='pipeline')

    op.alter_column('file_log', 'is_delivered',
                    server_default=sa.schema.DefaultClause('0'),
                    schema='pipeline')

    # ### end Alembic commands ###


def downgrade():

    op.drop_column('file_log', 'to_update', schema='pipeline')

    op.alter_column('file_log', 'is_archived',
                    server_default=None,
                    schema='pipeline')

    op.alter_column('file_log', 'is_delivered',
                    server_default=None,
                    schema='pipeline')
