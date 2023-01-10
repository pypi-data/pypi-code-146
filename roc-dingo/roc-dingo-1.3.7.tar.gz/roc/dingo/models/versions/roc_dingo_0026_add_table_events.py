# -*- coding: utf-8 -*-
"""empty message

Revision ID: roc_dingo_0025_add_table_events
Revises: roc_dingo_0025_add_views_for_anomalies
Create Date: 2022-11-14 17:02:37.168657

"""
from alembic import op
import sqlalchemy as sa
from pathlib import Path
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'roc_dingo_0026_add_table_events'
down_revision = 'roc_dingo_0025_add_views_for_anomalies'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'events',
        sa.Column('id', sa.BIGINT(), nullable=False),
        sa.Column('label', sa.String(), nullable=False),
        sa.Column('is_tracked', sa.BOOLEAN(), nullable=False),
        sa.Column('is_anomaly', sa.BOOLEAN(), nullable=False),
        sa.Column('origin', postgresql.ENUM(
            'SOLO', 'RPW', name='event_origin_enum'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('label'),
        schema='pipeline'
    )

    # set default values
    op.alter_column('events', 'is_tracked',
                    server_default=sa.schema.DefaultClause('1'),  # true
                    schema='pipeline')
    op.alter_column('events', 'is_anomaly',
                    server_default=sa.schema.DefaultClause('0'),  # false
                    schema='pipeline')

    op.execute('DROP VIEW IF EXISTS pipeline.anomalies_per_day')
    op.drop_table('anomalies', schema='pipeline')

    # insert data into events
    filename = 'SQL/roc_dingo_0026_insert_into_events.sql'
    sql_insert_file = Path(__file__).parent / filename
    with open(sql_insert_file, 'r') as sql_file:
        sql_cmd = sql_file.read()
        op.execute(sql_cmd)

    # create views
    filename = 'SQL/roc_dingo_0026_create_view_anomalies_per_day.sql'
    sql_file = Path(__file__).parent / filename
    with open(sql_file, 'r') as sql_content:
        sql_cmd = sql_content.read()
        op.execute(sql_cmd)

    filename = 'SQL/roc_dingo_0026_create_view_rpw_events_per_day.sql'
    sql_file = Path(__file__).parent / filename
    with open(sql_file, 'r') as sql_content:
        sql_cmd = sql_content.read()
        op.execute(sql_cmd)


def downgrade():

    # anomalies_per_day depends on events, delete it first
    op.execute('DROP VIEW IF EXISTS pipeline.anomalies_per_day')
    op.execute('DROP VIEW IF EXISTS pipeline.rpw_events_per_day')
    op.drop_table('events', schema='pipeline')

    # drop enumeration
    op.execute('DROP TYPE IF EXISTS event_origin_enum;')

    # Re create anomalies
    op.create_table('anomalies',
                    sa.Column('id', sa.BIGINT(), nullable=False),
                    sa.Column('label', sa.String(), nullable=False),
                    sa.Column('tracked', sa.BOOLEAN(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('label'),
                    schema='pipeline')

    # set default value to TRUE
    op.alter_column('anomalies', 'tracked',
                    server_default=sa.schema.DefaultClause('1'),
                    schema='pipeline')

    # insert data into anomalies
    filename = 'SQL/roc_dingo_0025_insert_into_anomalies.sql'
    sql_insert_file = Path(__file__).parent / filename
    with open(sql_insert_file, 'r') as sql_file:
        sql_cmd = sql_file.read()
        op.execute(sql_cmd)

    # recreate view anomalies_per_day
    filename = 'SQL/roc_dingo_0025_create_view_anomalies_per_day.sql'
    sql_file = Path(__file__).parent / filename
    with open(sql_file, 'r') as sql_content:
        sql_cmd = sql_content.read()
        op.execute(sql_cmd)
