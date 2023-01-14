# -*- coding: utf-8; -*-
"""add upgrade.system

Revision ID: 363a96293285
Revises: 0848a1761233
Create Date: 2022-08-19 18:00:43.843663

"""

# revision identifiers, used by Alembic.
revision = '363a96293285'
down_revision = '0848a1761233'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # upgrade
    op.add_column('upgrade', sa.Column('system', sa.String(length=100), nullable=True))


def downgrade():

    # upgrade
    op.drop_column('upgrade', 'system')
