# -*- coding: utf-8 -*-
"""Add views to display data grouped by date

Revision ID: roc_dingo_0010_add_view
Revises: roc_dingo_0009_add_bia
Create Date: 2021-06-14 11:29:28.513231

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'roc_dingo_0010_add_view'
down_revision = 'roc_dingo_0009_add_bia'
branch_labels = None
depends_on = None


def upgrade():

    op.execute('COMMIT')
    op.execute("""CREATE OR REPLACE VIEW pipeline.file_log_per_date AS
        select date(start_time) as date,
            count(state='OK' or null) as OK,
            count(state='ERROR' or null) as ERROR,
            count(state='WARNING' or null) as WARNING,
            count(*)
        from pipeline.file_log f1
        where f1.start_time is not null
        and f1.is_latest and not f1.is_removed
        group by (date(start_time))
        order by date
    """)

    op.execute("""CREATE OR REPLACE VIEW pipeline.file_log_per_date_wo_sk AS
        select date(start_time) as date,
            count(state='OK' or null) as OK,
            count(state='ERROR' or null) as ERROR,
            count(state='WARNING' or null) as WARNING,
            count(*)
        from pipeline.file_log f1
        where f1.start_time is not null
        and level != 'SK'
        and f1.is_latest and not f1.is_removed
        group by (date(start_time))
        order by date
    """)


def downgrade():

    op.execute('COMMIT')
    op.execute('DROP VIEW IF EXISTS pipeline.file_log_per_date')
    op.execute('DROP VIEW IF EXISTS pipeline.file_log_per_date_wo_sk')
