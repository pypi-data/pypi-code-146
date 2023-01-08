"""Класс содержит базовые иключения."""


class AlreadyUsedException(Exception):
    """Исключение для случая, когда пользователь делает два метода с одинаковым названием."""
    def __init__(self, func):
        self.message = f'Function {func.__name__} already used'
        super().__init__(self.message)


class InvalidParametersCount(Exception):
    """Исключение для случая, когда метод принимает неверное число аргументов."""
    def __init__(self, func, need, there_are):
        self.message = f'The "{func.__name__}" function accepts \
            {there_are} parameters, but must have {need}'
        super().__init__(self.message)
