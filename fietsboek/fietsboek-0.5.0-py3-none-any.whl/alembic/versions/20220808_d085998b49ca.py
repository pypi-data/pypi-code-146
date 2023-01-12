"""Add track.type column.

Revision ID: d085998b49ca
Revises: 091ce24409fe
Create Date: 2022-08-08 14:11:40.746008

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'd085998b49ca'
down_revision = '091ce24409fe'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('tracks', sa.Column('type', sa.Enum('ORGANIC', 'SYNTHETIC', name='tracktype'), nullable=True))
    op.execute("UPDATE tracks SET type='ORGANIC';")

def downgrade():
    op.drop_column('tracks', 'type')
