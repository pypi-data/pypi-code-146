"""Add registration_allowed column to Tenant

Revision ID: 67c0904f3ebc
Revises: 8d7729f5ed1f
Create Date: 2022-10-28 13:24:29.274106

"""
import sqlalchemy as sa
from alembic import op

import fief

# revision identifiers, used by Alembic.
revision = "67c0904f3ebc"
down_revision = "8d7729f5ed1f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "fief_tenants",
        sa.Column(
            "registration_allowed", sa.Boolean(), nullable=False, server_default="1"
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("fief_tenants", "registration_allowed")
    # ### end Alembic commands ###
