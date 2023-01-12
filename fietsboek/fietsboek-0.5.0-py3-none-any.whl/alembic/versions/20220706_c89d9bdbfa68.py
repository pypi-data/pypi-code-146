"""Add timezone information to tracks

Revision ID: c89d9bdbfa68
Revises: 1b4b1c179e5a
Create Date: 2022-07-06 14:05:15.431716

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c89d9bdbfa68'
down_revision = '1b4b1c179e5a'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('track_cache', 'start_time', new_column_name='start_time_raw')
    op.alter_column('track_cache', 'end_time', new_column_name='end_time_raw')
    op.add_column('track_cache', sa.Column('start_time_tz', sa.Integer(), nullable=True))
    op.add_column('track_cache', sa.Column('end_time_tz', sa.Integer(), nullable=True))
    op.alter_column('tracks', 'date', new_column_name='date_raw')
    op.add_column('tracks', sa.Column('date_tz', sa.Integer(), nullable=True))

    op.execute('UPDATE tracks SET date_tz=0;')
    op.execute('UPDATE track_cache SET start_time_tz=0, end_time_tz=0;')


def downgrade():
    op.alter_column('tracks', 'date_raw', new_column_name='date')
    op.drop_column('tracks', 'date_tz')
    op.alter_column('track_cache', 'start_time_raw', new_column_name='start_time')
    op.alter_column('track_cache', 'end_time_raw', new_column_name='end_time')
    op.drop_column('track_cache', 'start_time_tz')
    op.drop_column('track_cache', 'end_time_tz')
