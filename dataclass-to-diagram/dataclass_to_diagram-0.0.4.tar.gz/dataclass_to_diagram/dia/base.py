"""Базовая диаграмма."""

from typing import NamedTuple

from typing_extensions import Self


class Image(NamedTuple):
    """Изображение с имененем файла."""

    filename: str
    content: bytes


class BaseDiagram:
    """Базовая диаграмма.

    Все диаграммы должны наследовать от этого класса
    """

    def __init__(
        self: "BaseDiagram",
        filename: str,
    ) -> None:
        """Создать объект базовой диаграммы.

        :param filename: имя создаваемого файла
        """
        self.__filename = filename

    @property
    def filename(self: "BaseDiagram") -> str:
        """Возвращает имя файла (без расширения).

        :return: имя файла
        """
        return self.__filename

    def get_images(self: Self) -> tuple[Image]:
        """Возвращает кортеж изображений.

        :raises NotImplementedError: Функция не определена
        """
        raise NotImplementedError("Функция не определена.")

    def _get_text_file(self: "BaseDiagram", ext: str = ".puml") -> Image:
        """Возвращает текстовый файл.

        :param ext: расширение для текстового файла
        :return: текстовый файл
        """
        return Image(
            filename=self.filename + ext,
            content=bytes(repr(self).encode()),
        )
