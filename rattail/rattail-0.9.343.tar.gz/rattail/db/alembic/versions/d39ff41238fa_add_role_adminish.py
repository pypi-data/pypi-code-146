# -*- coding: utf-8 -*-
"""add role.adminish

Revision ID: d39ff41238fa
Revises: 363a96293285
Create Date: 2022-08-21 19:29:09.547336

"""

# revision identifiers, used by Alembic.
revision = 'd39ff41238fa'
down_revision = '363a96293285'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # role
    op.add_column('role', sa.Column('adminish', sa.Boolean(), nullable=True))
    op.add_column('role_version', sa.Column('adminish', sa.Boolean(), autoincrement=False, nullable=True))


def downgrade():

    # role
    op.drop_column('role_version', 'adminish')
    op.drop_column('role', 'adminish')
