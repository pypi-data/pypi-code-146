from typing import Optional

from lnschema_core.dev.sqlmodel import schema_sqlmodel
from sqlmodel import Field, ForeignKeyConstraint

from . import _name as schema_name
from .dev import id as idg

SQLModel, prefix, schema_arg = schema_sqlmodel(schema_name)


class Pipeline(SQLModel, table=True):  # type: ignore
    """Bioinformatics pipelines."""

    __tablename__ = f"{prefix}pipeline"

    __table_args__ = (
        ForeignKeyConstraint(
            ["id", "v"],
            ["core.pipeline.id", "core.pipeline.v"],
        ),
        {"schema": schema_arg},
    )
    id: str = Field(primary_key=True, index=True)
    v: str = Field(primary_key=True, index=True)


class Run(SQLModel, table=True):  # type: ignore
    """Bioinformatics pipeline runs."""

    __tablename__ = f"{prefix}run"
    __table_args__ = (
        ForeignKeyConstraint(
            ["pipeline_id", "pipeline_v"],
            ["bfx.pipeline.id", "bfx.pipeline.v"],
        ),
        {"schema": schema_arg},
    )
    id: str = Field(primary_key=True, foreign_key="core.run.id", index=True)
    dir: Optional[str] = None
    pipeline_id: str = Field(index=True)
    pipeline_v: str = Field(index=True)


class Bfxmeta(SQLModel, table=True):  # type: ignore
    """Metadata for files associated with bioinformatics pipelines."""

    id: Optional[str] = Field(default_factory=idg.bfxmeta, primary_key=True)
    file_type: Optional[str] = None
    dir: Optional[str] = None


class DObjectBfxmeta(SQLModel, table=True):  # type: ignore
    """Link table between dobject and bfxmeta tables."""

    __tablename__ = f"{prefix}dobject_bfxmeta"
    dobject_id: str = Field(primary_key=True, foreign_key="core.dobject.id")
    bfxmeta_id: str = Field(primary_key=True, foreign_key="bfx.bfxmeta.id")
