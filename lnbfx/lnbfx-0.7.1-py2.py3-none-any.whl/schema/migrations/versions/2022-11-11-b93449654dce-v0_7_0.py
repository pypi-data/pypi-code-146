"""v0.7.0.

Revision ID: b93449654dce
Revises: cfda12fc80a8
Create Date: 2022-11-11 14:56:08.665667

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b93449654dce"
down_revision = "cfda12fc80a8"
branch_labels = None
depends_on = None


def upgrade_sqlite():
    op.rename_table("bfx.bfx_pipeline", "bfx.pipeline")
    op.rename_table("bfx.bfx_run", "bfx.run")
    op.alter_column(
        "bfx.run", column_name="bfx_pipeline_id", new_column_name="pipeline_id"
    )
    op.alter_column(
        "bfx.run", column_name="bfx_pipeline_v", new_column_name="bfx_pipeline_v"
    )


def upgrade_postgres():
    op.rename_table("bfx_pipeline", "pipeline", schema="bfx")
    op.rename_table("bfx_run", "run", schema="bfx")
    op.alter_column(
        "run",
        column_name="bfx_pipeline_id",
        new_column_name="pipeline_id",
        schema="bfx",
    )
    op.alter_column(
        "run",
        column_name="bfx_pipeline_v",
        new_column_name="pipeline_v",
        schema="bfx",
    )


def upgrade() -> None:
    bind = op.get_bind()
    if bind.engine.name == "sqlite":
        upgrade_sqlite()
        pass
    else:
        upgrade_postgres()


def downgrade() -> None:
    pass
