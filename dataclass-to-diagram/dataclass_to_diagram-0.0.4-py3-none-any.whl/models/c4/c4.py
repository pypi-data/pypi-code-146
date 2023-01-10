from dataclasses import dataclass
from typing import Sequence

from ..base_model import BaseModel

from .base import BaseContainer, BaseContext, BaseRel, BaseSprite
from .tag import ElementTag, RelationTag


@dataclass
class C4(BaseModel):
    contexts: Sequence[BaseContext] | None = None
    containers: Sequence[BaseContainer] | None = None
    relations: Sequence[BaseRel] | None = None
    show_legend: bool = True

    def find_all_sprites(self) -> set[BaseSprite]:
        """Возвращает все спрайты."""
        sprites: set[BaseSprite] = set()
        if self.contexts:
            for context in self.contexts:
                sprites.update(context.find_all_sprites())
        if self.containers:
            for container in self.containers:
                sprites.update(container.find_all_sprites())
        return sprites

    def find_all_element_tags(self) -> set[ElementTag]:
        """Возращает все теги элементов."""
        tags: set[ElementTag] = set()
        if self.contexts:
            for context in self.contexts:
                tags.update(context.find_all_tags())
        if self.containers:
            for container in self.containers:
                tags.update(container.find_all_tags())
        return tags

    def find_all_relation_tags(self) -> set[RelationTag]:
        """Возращает все теги отношений."""
        tags: set[RelationTag] = set()
        if self.relations is None:
            return tags
        for relation in self.relations:
            if relation.tags is None:
                continue
            tags.update(relation.tags)
        return tags
