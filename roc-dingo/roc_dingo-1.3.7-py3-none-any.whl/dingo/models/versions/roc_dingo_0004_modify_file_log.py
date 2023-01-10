# -*- coding: utf-8 -*-
"""Modify file_log table


Revision ID: roc_dingo_0004_modify_file_log
Revises: roc_dingo_0003_add_cascade
Create Date: 2020-07-28 09:12:14.769013

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from poppy.pop.alembic.helpers import create_table, drop_table, execute, user

# revision identifiers, used by Alembic.
revision = 'roc_dingo_0004_modify_file_log'
# down_revision = 'roc_dingo_0003_add_cascade'
down_revision = 'roc_dingo_0001_initial'
depends_on = None


def upgrade():
    # rename columns
    op.alter_column(
        'file_log', 'id_file_log',
        new_column_name='id', schema='pipeline')
    op.alter_column(
        'file_log', 'file_author',
        new_column_name='author', schema='pipeline')
    op.alter_column(
        'file_log', 'file_basename',
        new_column_name='basename', schema='pipeline')
    op.alter_column(
        'file_log', 'file_creation_date',
        new_column_name='creation_time', schema='pipeline')
    op.alter_column(
        'file_log', 'file_dataset_id',
        new_column_name='dataset_id', schema='pipeline')
    op.alter_column(
        'file_log', 'file_date',
        new_column_name='date', schema='pipeline')
    op.alter_column(
        'file_log', 'file_descr',
        new_column_name='descr', schema='pipeline')
    op.alter_column(
        'file_log', 'file_dir',
        new_column_name='dirname', schema='pipeline')
    op.alter_column(
        'file_log', 'file_endtime',
        new_column_name='end_time', schema='pipeline')
    op.alter_column(
        'file_log', 'file_insert_date',
        new_column_name='insert_time', schema='pipeline')
    op.alter_column(
        'file_log', 'file_sha',
        new_column_name='sha', schema='pipeline')
    op.alter_column(
        'file_log', 'file_size',
        new_column_name='size', schema='pipeline')
    op.alter_column(
        'file_log', 'file_starttime',
        new_column_name='start_time', schema='pipeline')
    op.alter_column(
        'file_log', 'file_state',
        new_column_name='state', schema='pipeline')
    op.alter_column(
        'file_log', 'file_status',
        new_column_name='status', schema='pipeline')
    op.alter_column(
        'file_log', 'file_url',
        new_column_name='url', schema='pipeline')
    op.alter_column(
        'file_log', 'file_version',
        new_column_name='version', schema='pipeline')

    op.drop_constraint(
        'file_log_file_basename_key', 'file_log',
        schema='pipeline', type_='unique')
    op.create_unique_constraint(
        'file_log_basename_key', 'file_log', ['basename'], schema='pipeline')

    # Very dirty hack because SA does not create
    # ENUM types when add_column, only with create_table
    # https://stackoverflow.com/questions/47206201/
    # how-to-use-enum-with-sqlalchemy-and-alembic
    # after deletting the table, the enum type is kept

    op.create_table(
        'dirty_hack',
        sa.Column('id', sa.BIGINT(), primary_key=True),
        sa.Column(
            'type',
            postgresql.ENUM(
                'CAL', 'HK', 'L0', 'L1', 'L1R', 'L2',
                'L3', 'LL01', 'TC', 'TM',
                name='file_type_list',
                )),
        schema='pipeline'
    )
    op.drop_table('dirty_hack', schema='pipeline')

    op.add_column('file_log', sa.Column(
        'type',
        postgresql.ENUM(
            'CAL', 'HK', 'L0', 'L1', 'L1R',
            'L2', 'L3', 'LL01', 'TC', 'TM',
            name='file_type_list'),
        autoincrement=False, nullable=False), schema='pipeline')
    op.add_column(
        'file_log', sa.Column('is_latest', sa.BOOLEAN(), nullable=False),
        schema='pipeline')
    op.add_column(
        'file_log', sa.Column('validity_end', postgresql.TIMESTAMP()),
        schema='pipeline')
    op.add_column(
        'file_log', sa.Column('validity_start', postgresql.TIMESTAMP()),
        schema='pipeline')

    op.drop_column('file_log', 'file_name', schema='pipeline')
    op.drop_column('file_log', 'is_test', schema='pipeline')
    op.drop_column('file_log', 'file_parents', schema='pipeline')
    op.drop_column('file_log', 'file_id', schema='pipeline')
    op.drop_column('file_log', 'file_level', schema='pipeline')

    # Start and stop time can be null
    op.alter_column(
        'file_log', 'start_time',
        nullable=True, schema='pipeline')
    op.alter_column(
        'file_log', 'end_time',
        nullable=True, schema='pipeline')

    # create parents table
    create_table(
        'parents_file_log',
        sa.Column('id', sa.BIGINT(), nullable=False),
        sa.Column('id_child', sa.BIGINT(), nullable=False),
        sa.Column('id_parent', sa.BIGINT(), nullable=False),
        sa.ForeignKeyConstraint(
            ['id_child'], ['pipeline.file_log.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(
            ['id_parent'], ['pipeline.file_log.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id_child', 'id_parent'),
        schema='pipeline'
    )
    # ### end Alembic commands ###

    # fix table permissions
    grant_user_seq = (
        """GRANT USAGE, SELECT
        ON ALL SEQUENCES IN SCHEMA pipeline TO {0}""".format(user)
    )
    execute(grant_user_seq)


def downgrade():
    # first drop parents_file_log table
    drop_table('parents_file_log', schema='pipeline')

    # Start and stop time cannot be null
    op.alter_column(
        'file_log', 'start_time',
        nullable=False, schema='pipeline')
    op.alter_column(
        'file_log', 'end_time',
        nullable=False, schema='pipeline')

    # rename columns

    op.alter_column(
        'file_log', 'id',
        new_column_name='id_file_log', schema='pipeline')
    op.alter_column(
        'file_log', 'author',
        new_column_name='file_author', schema='pipeline')
    op.alter_column(
        'file_log', 'basename',
        new_column_name='file_basename', schema='pipeline')
    op.alter_column(
        'file_log', 'creation_time',
        new_column_name='file_creation_date', schema='pipeline')
    op.alter_column(
        'file_log', 'dataset_id',
        new_column_name='file_dataset_id', schema='pipeline')
    op.alter_column(
        'file_log', 'date',
        new_column_name='file_date', schema='pipeline')
    op.alter_column(
        'file_log', 'descr',
        new_column_name='file_descr', schema='pipeline')
    op.alter_column(
        'file_log', 'dirname',
        new_column_name='file_dir', schema='pipeline')
    op.alter_column(
        'file_log', 'end_time',
        new_column_name='file_endtime', schema='pipeline')
    op.alter_column(
        'file_log', 'insert_time',
        new_column_name='file_insert_date', schema='pipeline')
    op.alter_column(
        'file_log', 'sha',
        new_column_name='file_sha', schema='pipeline')
    op.alter_column(
        'file_log', 'size',
        new_column_name='file_size', schema='pipeline')
    op.alter_column(
        'file_log', 'start_time',
        new_column_name='file_starttime', schema='pipeline')
    op.alter_column(
        'file_log', 'state',
        new_column_name='file_state', schema='pipeline')
    op.alter_column(
        'file_log', 'status',
        new_column_name='file_status', schema='pipeline')
    op.alter_column(
        'file_log', 'url',
        new_column_name='file_url', schema='pipeline')
    op.alter_column(
        'file_log', 'version',
        new_column_name='file_version', schema='pipeline')

    op.drop_constraint(
        'file_log_basename_key', 'file_log',
        schema='pipeline', type_='unique')
    op.create_unique_constraint(
        'file_log_file_basename_key', 'file_log',
        ['file_basename'], schema='pipeline')

    op.drop_column('file_log', 'type', schema='pipeline')
    op.drop_column('file_log', 'is_latest', schema='pipeline')
    op.drop_column('file_log', 'validity_end', schema='pipeline')
    op.drop_column('file_log', 'validity_start', schema='pipeline')

    execute('DROP TYPE IF EXISTS file_type_list')

    op.add_column(
        'file_log',
        sa.Column('file_id', sa.String(length=48), nullable=False),
        schema='pipeline')
    op.add_column(
        'file_log',
        sa.Column('file_level', sa.String(length=8), nullable=False),
        schema='pipeline')
    op.add_column(
        'file_log',
        sa.Column(
            'file_parents', sa.VARCHAR(length=512),
            autoincrement=False, nullable=True),
        schema='pipeline')
    op.add_column(
        'file_log',
        sa.Column(
            'is_test', sa.BOOLEAN(),
            autoincrement=False, nullable=False),
        schema='pipeline')
    op.add_column(
        'file_log', sa.Column(
            'file_name', sa.VARCHAR(length=512),
            autoincrement=False, nullable=True),
        schema='pipeline')

    # ### end Alembic commands ###
