"""Генерировать уникальные alias для элементов."""


class AliasFenerator(object):
    """Генерировать уникальные alias для элементов."""

    def __init__(self) -> None:
        """Создать генератор alias."""
        self.__alias = 0

    def new_alias(self) -> int:
        """Генерировать новый alias."""
        self.__alias += 1
        return self.__alias
