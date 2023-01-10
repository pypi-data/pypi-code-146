from typing import Iterable
from dataclass_to_diagram.models.c4.base import BaseSprite


def sprites_to_puml(sprites: Iterable[BaseSprite] | None) -> str:
    if not sprites:
        return ""
    sprites_includes: set[str] = set()
    for sprite in sprites:
        sprites_includes.update(sprite.include_statements_for_sprite())
    return "\n" + "\n".join(sorted(sprites_includes))
