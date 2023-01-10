class BaseError(Exception):
    pass


class IncorrectArgError(BaseError):
    pass


class ConverterError(BaseError):
    """Ошибка конвертирования файла."""

    pass
