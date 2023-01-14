# -*- coding: utf-8; -*-
"""add tailbone_page_help

Revision ID: 31b0b868d6f0
Revises: 4594843ad852
Create Date: 2022-12-24 14:04:59.538930

"""

# revision identifiers, used by Alembic.
revision = '31b0b868d6f0'
down_revision = '4594843ad852'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # tailbone_page_help
    op.create_table('tailbone_page_help',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('route_prefix', sa.String(length=254), nullable=False),
                    sa.Column('help_url', sa.String(length=254), nullable=True),
                    sa.Column('markdown_text', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('uuid'),
                    sa.UniqueConstraint('route_prefix', name='tailbone_page_help_uq_route_prefix')
    )
    op.create_table('tailbone_page_help_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('route_prefix', sa.String(length=254), autoincrement=False, nullable=True),
                    sa.Column('help_url', sa.String(length=254), autoincrement=False, nullable=True),
                    sa.Column('markdown_text', sa.Text(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_tailbone_page_help_version_end_transaction_id'), 'tailbone_page_help_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_tailbone_page_help_version_operation_type'), 'tailbone_page_help_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_tailbone_page_help_version_transaction_id'), 'tailbone_page_help_version', ['transaction_id'], unique=False)

    # tailbone_field_info
    op.create_table('tailbone_field_info',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('route_prefix', sa.String(length=254), nullable=False),
                    sa.Column('field_name', sa.String(length=100), nullable=False),
                    sa.Column('markdown_text', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('uuid'),
                    sa.UniqueConstraint('route_prefix', 'field_name', name='tailbone_field_info_uq_field')
    )
    op.create_table('tailbone_field_info_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('route_prefix', sa.String(length=254), autoincrement=False, nullable=True),
                    sa.Column('field_name', sa.String(length=100), autoincrement=False, nullable=True),
                    sa.Column('markdown_text', sa.Text(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_tailbone_field_info_version_end_transaction_id'), 'tailbone_field_info_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_tailbone_field_info_version_operation_type'), 'tailbone_field_info_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_tailbone_field_info_version_transaction_id'), 'tailbone_field_info_version', ['transaction_id'], unique=False)


def downgrade():

    # tailbone_field_info
    op.drop_index(op.f('ix_tailbone_field_info_version_transaction_id'), table_name='tailbone_field_info_version')
    op.drop_index(op.f('ix_tailbone_field_info_version_operation_type'), table_name='tailbone_field_info_version')
    op.drop_index(op.f('ix_tailbone_field_info_version_end_transaction_id'), table_name='tailbone_field_info_version')
    op.drop_table('tailbone_field_info_version')
    op.drop_table('tailbone_field_info')

    # tailbone_page_help
    op.drop_index(op.f('ix_tailbone_page_help_version_transaction_id'), table_name='tailbone_page_help_version')
    op.drop_index(op.f('ix_tailbone_page_help_version_operation_type'), table_name='tailbone_page_help_version')
    op.drop_index(op.f('ix_tailbone_page_help_version_end_transaction_id'), table_name='tailbone_page_help_version')
    op.drop_table('tailbone_page_help_version')
    op.drop_table('tailbone_page_help')
