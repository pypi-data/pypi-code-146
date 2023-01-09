"""v0.5.0.

Revision ID: cfda12fc80a8
Revises: None
Create Date: 2022-11-03
"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

revision = "cfda12fc80a8"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.engine.name == "sqlite":
        op.rename_table(
            old_table_name="bfx_pipeline", new_table_name="bfx.bfx_pipeline"
        )
        op.rename_table(old_table_name="bfx_run", new_table_name="bfx.bfx_run")
        op.rename_table(old_table_name="bfxmeta", new_table_name="bfx.bfxmeta")
        op.rename_table(
            old_table_name="dobject_bfxmeta", new_table_name="bfx.dobject_bfxmeta"
        )
    else:
        op.execute("alter table public.bfx_pipeline set schema bfx")
        op.execute("alter table public.bfx_run set schema bfx")
        op.execute("alter table public.bfxmeta set schema bfx")
        op.execute("alter table public.dobject_bfxmeta set schema bfx")


def downgrade() -> None:
    pass
