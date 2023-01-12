"""add image metadata to uploads

Revision ID: 091ce24409fe
Revises: c89d9bdbfa68
Create Date: 2022-07-21 23:24:54.241170

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '091ce24409fe'
down_revision = 'c89d9bdbfa68'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('image_metadata',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('track_id', sa.Integer(), nullable=False),
    sa.Column('image_name', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['track_id'], ['tracks.id'], name=op.f('fk_image_metadata_track_id_tracks')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_image_metadata')),
    sa.UniqueConstraint('track_id', 'image_name', name=op.f('uq_image_metadata_track_id'))
    )

def downgrade():
    op.drop_table('image_metadata')
