"""Диаграмма состояний.

Описание - https://mermaid-js.github.io/mermaid/#/stateDiagram

Не поддерживается:
- concurrency
- direction
"""

import logging
from enum import Enum

from dataclass_to_diagram.dia.base import BaseDiagram
from dataclass_to_diagram.dia.base import Image

from typing_extensions import Self

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


TEMPL_DIA: str = """stateDiagram-v2
{states}
{trans}"""
TEMPL_STATE1: str = "{label}"
TEMPL_STATE2: str = """state {label} {{
{states}
{trans}
}}"""  # noqa: JS101
TEMPL_STATE3: str = "state {label} {modif}"
TEMPL_TRANS: str = "{begin} --> {end} {desc}"
TEMPL_NOTE: str = """note {pos} of {state}
{text}
end note"""


class Note:
    """Пояснение к состоянию."""

    class PosEnum(Enum):
        """Положение заметки."""

        left = "left"
        right = "right"

    __text: str
    __pos: PosEnum
    __state_label: str

    def __init__(self: Self, text: str, pos: PosEnum = PosEnum.left) -> None:
        """Пояснение к состоянию.

        :param text: текст пояснения
        :param pos: положение пояснения, слева или справа
        """
        self.__text = text
        self.__pos = pos

    def set_state_label(self: Self, label: str) -> None:
        """Установить название состояния.

        :param label: название состояния
        """
        self.__state_label = label

    def __repr__(self: Self) -> str:
        """Represent as string.

        :return: string representation
        """
        return TEMPL_NOTE.format(
            pos=self.__pos.value,
            state=self.__state_label,
            text=self.__text,
        )


class State:
    """Состояние."""

    class ModifEnum(Enum):
        """Разновидности состояний."""

        standard = ""
        choice = "<<choice>>"
        fork = "<<fork>>"
        join = "<<join>>"

    __label: str
    __states: list[Self] | None
    __trans: list["Trans"] | None
    __modif: ModifEnum
    __note: Note | None

    def __init__(
        self: Self,
        label: str,
        states: list[Self] | None = None,
        trans: list["Trans"] | None = None,
        modif: ModifEnum = ModifEnum.standard,
        note: Note | None = None,
    ) -> None:
        """Состояние.

        :param label: название состояния
        :param states: список состояний
        :param trans: список переходов
        :param modif: модификатор ModifEnum
        :param note: пояснение
        """
        self.__label = label
        self.__states = states
        self.__trans = trans
        self.__modif = modif
        self.__note = note
        if self.__note is not None:
            self.__note.set_state_label(self.__label)

    @property
    def label(self: Self) -> str:
        """Label.

        :return: label
        """
        return self.__label

    def __repr__(self: Self) -> str:
        """Represent as string.

        :return: string representation
        """
        out: str = ""
        if self.__states is not None and self.__trans is not None:
            out += TEMPL_STATE2.format(
                label=self.__label,
                states="\n".join([repr(s) for s in self.__states]),
                trans="\n".join([repr(t) for t in self.__trans]),
            )
        elif self.__modif == self.ModifEnum.standard:
            out += TEMPL_STATE1.format(
                label=self.__label,
            )
        else:
            out += TEMPL_STATE3.format(
                label=self.__label,
                modif=self.__modif.value,
            )
        if self.__note is not None:
            out += "\n" + repr(self.__note)
        return out


class Trans:
    """Переход."""

    __begin: State | None
    __end: State | None
    __desc: str

    def __init__(
        self: Self,
        begin: State | None,
        end: State | None,
        desc: str = "",
    ) -> None:
        """Переход.

        :param begin: начальное состояние
        :param end: конечное состояние
        :param desc: описание
        """
        self.__begin = begin
        self.__end = end
        self.__desc = desc

    def __repr__(self: Self) -> str:
        """Reperesent as string.

        :return: string representation
        """
        return TEMPL_TRANS.format(
            begin=self.__begin.label if self.__begin is not None else "[*]",
            end=self.__end.label if self.__end is not None else "[*]",
            desc=": " + self.__desc if self.__desc else "",
        )


class Diagram(BaseDiagram):
    """Класс диаграммы."""

    __states: list[State]
    __trans: list[Trans]

    def __init__(
        self: Self,
        filename: str,
        states: list[State],
        trans: list[Trans],
    ) -> None:
        """Класс диаграммы.

        :param filename: имя файла
        :param states: список состояний
        :param trans: список переходов
        """
        super().__init__(filename)
        self.__states = states
        self.__trans = trans

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
        return TEMPL_DIA.format(
            states="\n".join([repr(s) for s in self.__states]),
            trans="\n".join([repr(t) for t in self.__trans]),
        )
