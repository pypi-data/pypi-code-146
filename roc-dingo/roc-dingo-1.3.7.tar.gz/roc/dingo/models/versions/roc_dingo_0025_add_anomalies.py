# -*- coding: utf-8 -*-
"""empty message

Revision ID: roc_dingo_0025_add_views_for_anomalies
Revises: roc_dingo_0024_add_invalidpacketlog
Create Date: 2022-07-28 09:35:17.202789

"""
from alembic import op
import sqlalchemy as sa
from pathlib import Path

# revision identifiers, used by Alembic.
revision = 'roc_dingo_0025_add_views_for_anomalies'
down_revision = 'roc_dingo_0024_add_invalidpacketlog'
branch_labels = None
depends_on = None


def upgrade():
    # ensure commands are executed now
    # op.execute('COMMIT')

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

    # create views
    filename = 'SQL/roc_dingo_0025_create_view_anomalies_per_day.sql'
    sql_file = Path(__file__).parent / filename
    with open(sql_file, 'r') as sql_content:
        sql_cmd = sql_content.read()
        op.execute(sql_cmd)

    filename = 'SQL/roc_dingo_0025_create_view_total_events.sql'
    sql_file = Path(__file__).parent / filename
    with open(sql_file, 'r') as sql_content:
        sql_cmd = sql_content.read()
        op.execute(sql_cmd)


def downgrade():
    # op.execute('COMMIT')
    op.execute('DROP VIEW IF EXISTS pipeline.total_events')
    op.execute('DROP VIEW IF EXISTS pipeline.anomalies_per_day')
    op.drop_table('anomalies', schema='pipeline')
