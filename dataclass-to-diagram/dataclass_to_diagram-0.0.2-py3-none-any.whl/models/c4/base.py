"""Базовые классы модели."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Iterable, Sequence

from ..alias_generator import AliasFenerator


class BaseSprite(StrEnum):
    """Базовый класс для изображений."""

    def include_statements_for_sprite(self) -> set[str]:
        """Возвращает include для спрайтов."""
        raise NotImplementedError


@dataclass(frozen=True)
class BaseTag(object):
    """Базовый класс для тегов."""

    tag_stereo: str
    legend_text: str | None = None

    def __hash__(self) -> int:
        """Хеширование по названию тега."""
        return hash(self.tag_stereo)

    def __eq__(self, other: object) -> bool:
        """Равенство по названию тега."""
        if not isinstance(other, BaseTag):
            return False
        return self.tag_stereo == other.tag_stereo


@dataclass(frozen=True, eq=False)
class BaseElementTag(BaseTag):
    pass


@dataclass(frozen=True, eq=False)
class BaseRelationTag(BaseTag):
    pass


@dataclass(frozen=True, eq=False)
class BaseBoundaryTag(BaseTag):
    pass


@dataclass(frozen=True)
class BaseElement(ABC):
    """Базовый класс для контекста, контейнера и компонента."""

    class_name_str: str = field(init=False, default="NotImplemented")
    alias: int = field(init=False, default_factory=AliasFenerator().new_alias)
    label: str
    descr: str | None = None
    techn: str | None = None
    sprite: BaseSprite | None = None
    link: str | None = None
    tags: Iterable[BaseElementTag] | None = None

    @abstractmethod
    def find_all_sprites(self) -> set[BaseSprite]:
        """Возвращает все спрайты."""
        sprites: set[BaseSprite] = set()
        if self.sprite is not None:
            sprites.add(self.sprite)
        return sprites

    @abstractmethod
    def find_all_tags(self) -> set[BaseElementTag]:
        """Возращает все теги."""
        tags: set[BaseElementTag] = set()
        if self.tags is not None:
            tags.update(self.tags)
        return tags


@dataclass(frozen=True)
class BaseComponent(BaseElement):
    """Уровень 3 - Component."""

    def find_all_sprites(self) -> set[BaseSprite]:  # noqa: WPS612
        """Возвращает все спрайты."""
        return super().find_all_sprites()

    def find_all_tags(self) -> set[BaseElementTag]:  # noqa: WPS612
        """Возращает все теги."""
        return super().find_all_tags()


@dataclass(frozen=True)
class BaseContainer(BaseElement):
    """Уровень 2 - Container."""

    components: Sequence[BaseComponent] | None = None

    def find_all_sprites(self) -> set[BaseSprite]:
        """Возвращает все спрайты."""
        sprites = super().find_all_sprites()
        if self.components is None:
            return sprites
        for component in self.components:
            sprites.update(component.find_all_sprites())
        return sprites

    def find_all_tags(self) -> set[BaseElementTag]:
        """Возращает все теги."""
        tags: set[BaseElementTag] = super().find_all_tags()
        if self.components is not None:
            for component in self.components:
                tags.update(component.find_all_tags())
        return tags


@dataclass(frozen=True)
class BaseContext(BaseElement):
    """Уровень 1 - Context."""

    techn: None = field(init=False, default=None)
    containers: Sequence[BaseContainer] | None = None

    def find_all_sprites(self) -> set[BaseSprite]:
        """Возвращает все спрайты."""
        sprites = super().find_all_sprites()
        if self.containers is None:
            return sprites
        for container in self.containers:
            sprites.update(container.find_all_sprites())
        return sprites

    def find_all_tags(self) -> set[BaseElementTag]:
        """Возращает все теги."""
        tags: set[BaseElementTag] = super().find_all_tags()
        if self.containers is not None:
            for container in self.containers:
                tags.update(container.find_all_tags())
        return tags


@dataclass(frozen=True)
class BaseRel(object):
    """Базовый класс для связи элементов."""

    class_name_str: str = field(init=False, default="NotImplemented")
    begin: BaseElement
    end: BaseElement
    label: str
    techn: str | None = None
    descr: str | None = None
    link: str | None = None
    tags: Iterable[BaseRelationTag] | None = None
