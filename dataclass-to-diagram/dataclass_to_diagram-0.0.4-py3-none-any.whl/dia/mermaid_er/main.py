"""Mermaid entity relations."""

import logging
from enum import Enum

from dataclass_to_diagram.dia.base import BaseDiagram
from dataclass_to_diagram.dia.base import Image
from dataclass_to_diagram.service import kroki

from typing_extensions import Self

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


TEMPLATE: str = """%%{{init: {{'theme':'neutral'}}}}%%
erDiagram
{rels}
{entities}
"""

TEMPLATE_REL: str = (
    "    {entity_left} {entity_left_card}--{entity_right_card}"
    " {entity_right} : {label}\n"
)

TEMPLATE_ATTR: str = "        {type} {name} {key} {comment}"

TEMPLATE_ENTITY: str = """    {name} {{
{attr}
    }}

"""


class Attr:
    """Атрибут."""

    class Keys(Enum):
        """Типы ключей атрибутов."""

        PK = "PK"
        FK = "FK"
        NO = ""

    class Types(Enum):
        """Тип атрибута."""

        INT = "int"
        STR = "str"
        DATETIME = "datetime"
        BOOL = "bool"
        REAL = "real"

    __ty: Types
    __name: str
    __key: Keys
    __comment: str

    def __init__(
        self: Self,
        name: str,
        ty: Types,
        comment: str = "",
        key: Keys = Keys.NO,
    ) -> None:
        """Атрибут.

        :param ty: тип данных
        :param name: название атрибута
        :param key: ключ
        :param comment: комментарий
        """
        self.__ty = ty
        self.__name = name
        self.__key = key
        self.__comment = comment

    def __repr__(self: Self) -> str:
        """Represend as string.

        :return: string representation
        """
        return TEMPLATE_ATTR.format(
            type=self.__ty.value,
            name=self.__name,
            key=self.__key.value,
            comment="" if not self.__comment else f'"{self.__comment}"',
        )


class Entity:
    """Entity."""

    __name: str
    __attr: list[Attr]

    def __init__(self: Self, name: str, attr: list[Attr]) -> None:
        """Entity.

        :param name: название
        :param attr: список атрибутов
        """
        self.__name = name
        self.__attr = attr

    @property
    def name(self: Self) -> str:
        """Название.

        :return: строка с названием
        """
        return self.__name

    def __repr__(self: Self) -> str:
        """Represend as string.

        :return: string representation
        """
        return TEMPLATE_ENTITY.format(
            name=self.__name,
            attr="\n".join([repr(a) for a in self.__attr]),
        )


class Relation:
    """Relation."""

    class Cardinalities(Enum):
        """Типы отношений."""

        c_0_1 = "|oo|"
        c_1 = "||||"
        c_0_inf = "}oo{"
        c_1_inf = "}||{"

    def __init__(
        self: Self,
        left: Entity,
        left_card: Cardinalities,
        right_card: Cardinalities,
        right: Entity,
        label: str = "label",
    ) -> None:
        """Relation.

        :param left: Entity слева
        :param right: Entity справа
        :param left_card: Cardinality of left entity
        :param right_card: Cardinality of right entity
        :param label: describes the relationship from the perspective
            of the first entity
        """
        self.__left = left
        self.__right = right
        self.__left_card = left_card
        self.__right_card = right_card
        self.__label = label

    @property
    def left(self: Self) -> Entity:
        """Entity слева.

        :return: entity слева
        """
        return self.__left

    @property
    def right(self: Self) -> Entity:
        """Entity справа.

        :return: entity справа
        """
        return self.__right

    def __repr__(self: Self) -> str:
        """Represend as string.

        :return: string representation
        """
        return TEMPLATE_REL.format(
            entity_left=self.__left.name,
            entity_left_card=self.__left_card.value[0:2],
            entity_right_card=self.__right_card.value[2:],
            entity_right=self.__right.name,
            label=self.__label,
        )


class Diagram(BaseDiagram):
    """Класс диаграммы."""

    __rels: list[Relation]

    def __init__(
        self: Self,
        filename: str,
        rels: list[Relation],
    ) -> None:
        """Класс диаграммы.

        :param filename: имя файла
        :param rels: список отношений между Entities
        """
        super().__init__(filename)
        self.__rels = rels

    def get_images(self: Self) -> tuple[Image]:
        """Возвращает кортеж изображений.

        :return: кортеж изображений
        """
        images: list[Image] = []
        text = repr(self)
        images.append(self._get_text_file(".puml"))
        try:
            for fmt in (kroki.OutputFormats.SVG,):
                images.append(
                    Image(
                        filename=self.filename + "." + fmt.value,
                        content=kroki.get_image(
                            source=text,
                            diagram_type=kroki.DiagramTypes.MERMAID,
                            output_format=fmt,
                        ),
                    ),
                )
        except RuntimeError as exc:
            logger.exception(exc)
        return tuple(images)

    def __repr__(self: Self) -> str:
        """Represent as string.

        :return: string representation
        """
        entities: set[Entity] = set()
        for rel in self.__rels:
            entities.add(rel.left)
            entities.add(rel.right)
        return TEMPLATE.format(
            rels="".join([repr(rel) for rel in self.__rels]),
            entities="".join([repr(e) for e in entities]),
        )
