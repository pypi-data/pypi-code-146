from dataclasses import dataclass

from ..base import BaseBoundaryTag, BaseElementTag, BaseRelationTag


@dataclass(frozen=True, eq=False)
class ElementTag(BaseElementTag):
    bg_color: str | None = None
    font_color: str | None = None
    border_color: str | None = None
    shadowing: str | None = None
    shape: str | None = None
    sprite: str | None = None
    techn: str | None = None
    legend_sprite: str | None = None


@dataclass(frozen=True, eq=False)
class RelationTag(BaseRelationTag):
    text_color: str | None = None
    line_color: str | None = None
    line_style: str | None = None
    sprite: str | None = None
    techn: str | None = None
    legend_sprite: str | None = None
    line_thickness: str | None = None


@dataclass(frozen=True, eq=False)
class BoundaryTag(BaseBoundaryTag):
    bg_color: str | None = None
    font_color: str | None = None
    border_color: str | None = None
    shadowing: str | None = None
    shape: str | None = None
    type_: str | None = None
