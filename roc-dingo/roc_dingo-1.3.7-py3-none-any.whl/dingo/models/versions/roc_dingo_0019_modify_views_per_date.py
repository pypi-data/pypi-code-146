# -*- coding: utf-8 -*-
"""Modify the view file_log_per_date
 - exclude CAL files from the count
 - try to guess the date with the filename if needed

Revision ID: roc_dingo_0018_modify_views_per_date
Revises: roc_dingo_0017_add_efecsevents
Create Date: 2021-11-22 16:59:56.553350

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'roc_dingo_0019_modify_views_per_date'
down_revision = 'roc_dingo_0018b_add_product_to_file_log'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('COMMIT')

    # ensure the date is correctly guessed
    # skip SK files from this monitoring as we do not produce them
    op.execute("""CREATE OR REPLACE VIEW pipeline.file_log_per_date AS
        select coalesce(
                date(f1.start_time),
                date(f1.end_time),
                case when f1.basename ~ '^.*_[0-9]{8}_V.*$' then
                    cast(regexp_replace(
                        f1.basename,
                        '^.*_([0-9]{4})([0-9]{2})([0-9]{2})_V.*$',
                        '\\1-\\2-\\3') as date)
                when f1.basename ~ '^.*_[0-9]{8}T[0-9]{6}\-[0-9]{8}T[0-9]{6}_V.*$' then
                    cast(regexp_replace(
                        f1.basename,
                        '^.*_V([0-9]{4})([0-9]{2})([0-9]{2})T[0-9]{6}\-.*$',
                        '\\1-\\2-\\3') as date)
                when f1.basename ~ '^.*_V[0-9]{14}\.xml$' then
                    cast(regexp_replace(
                        f1.basename,
                        '^.*_V([0-9]{4})([0-9]{2})([0-9]{2})[0-9]{6}\.xml$',
                        '\\1-\\2-\\3') as date)
                else null
                end
            ) as date,
            count(f1.state='OK' or null) as OK,
            count(f1.state='ERROR' or null) as ERROR,
            count(f1.state='WARNING' or null) as WARNING,
            count(*)
        from pipeline.file_log f1
        where f1.level NOT IN ( 'CAL', 'SK')
        and f1.is_latest and not f1.is_removed
        group by coalesce(
                date(f1.start_time),
                date(f1.end_time),
                case when f1.basename ~ '^.*_[0-9]{8}_V.*$' then
                    cast(regexp_replace(
                        f1.basename,
                        '^.*_([0-9]{4})([0-9]{2})([0-9]{2})_V.*$',
                        '\\1-\\2-\\3') as date)
                when f1.basename ~ '^.*_[0-9]{8}T[0-9]{6}\-[0-9]{8}T[0-9]{6}_V.*$' then
                    cast(regexp_replace(
                        f1.basename,
                        '^.*_V([0-9]{4})([0-9]{2})([0-9]{2})T[0-9]{6}\-.*$',
                        '\\1-\\2-\\3') as date)
                when f1.basename ~ '^.*_V[0-9]{14}\.xml$' then
                    cast(regexp_replace(
                        f1.basename,
                        '^.*_V([0-9]{4})([0-9]{2})([0-9]{2})[0-9]{6}\.xml$',
                        '\\1-\\2-\\3') as date)
                else null
                end
            )
        order by date
    """)

    # useless now (SK files skipped by default)
    op.execute('DROP VIEW IF EXISTS pipeline.file_log_per_date_wo_sk')

    # monitor files w/o warnings for missing SPICE_KERNELS attribute
    op.execute("""CREATE OR REPLACE VIEW pipeline.file_log_per_date_wo_sk_warn AS
        select coalesce(
                date(f1.start_time),
                date(f1.end_time),
                case when f1.basename ~ '^.*_[0-9]{8}_V.*$' then
                    cast(regexp_replace(
                        f1.basename,
                        '^.*_([0-9]{4})([0-9]{2})([0-9]{2})_V.*$',
                        '\\1-\\2-\\3') as date)
                when f1.basename ~ '^.*_[0-9]{8}T[0-9]{6}\-[0-9]{8}T[0-9]{6}_V.*$' then
                    cast(regexp_replace(
                        f1.basename,
                        '^.*_V([0-9]{4})([0-9]{2})([0-9]{2})T[0-9]{6}\-.*$',
                        '\\1-\\2-\\3') as date)
                when f1.basename ~ '^.*_V[0-9]{14}\.xml$' then
                    cast(regexp_replace(
                        f1.basename,
                        '^.*_V([0-9]{4})([0-9]{2})([0-9]{2})[0-9]{6}\.xml$',
                        '\\1-\\2-\\3') as date)
                else null
                end
            ) as date,
            count(f1.state='OK' or null) as OK,
            count(f1.state='ERROR' or null) as ERROR,
            count(f1.state='WARNING' or null) as WARNING,
            count(*)
        from pipeline.file_log f1
        where f1.level NOT IN ( 'CAL', 'SK')
        and f1.error_log != '''SPICE_KERNELS: NO_SUCH_ATTR: Named attribute not found in this CDF.'''
        and f1.is_latest and not f1.is_removed
        group by coalesce(
                date(f1.start_time),
                date(f1.end_time),
                case when f1.basename ~ '^.*_[0-9]{8}_V.*$' then
                    cast(regexp_replace(
                        f1.basename,
                        '^.*_([0-9]{4})([0-9]{2})([0-9]{2})_V.*$',
                        '\\1-\\2-\\3') as date)
                when f1.basename ~ '^.*_[0-9]{8}T[0-9]{6}\-[0-9]{8}T[0-9]{6}_V.*$' then
                    cast(regexp_replace(
                        f1.basename,
                        '^.*_V([0-9]{4})([0-9]{2})([0-9]{2})T[0-9]{6}\-.*$',
                        '\\1-\\2-\\3') as date)
                when f1.basename ~ '^.*_V[0-9]{14}\.xml$' then
                    cast(regexp_replace(
                        f1.basename,
                        '^.*_V([0-9]{4})([0-9]{2})([0-9]{2})[0-9]{6}\.xml$',
                        '\\1-\\2-\\3') as date)
                else null
                end
            )
        order by date
    """)


def downgrade():

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

    op.execute('DROP VIEW IF EXISTS pipeline.file_log_per_date_wo_sk_warn')
