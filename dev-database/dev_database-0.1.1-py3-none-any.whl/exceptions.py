class InvalidDatabase(Exception):
    "Raised when an invalid Database was given"

    def __init__(self, database: str, message="") -> None:
        if message == "":
            message = f'The Database "{database}" couldnt be opened'
        super().__init__(message)


class NotSavePath(Exception):
    "Raised when the function self.is_path_save says that your input is not save"

    def __init__(self, path: str, message="") -> None:
        if message == "":
            message = f'The Path "{path}" is not save'
        super().__init__(message)


class CorruptDatabaseStructure(Exception):
    "Raised when the function self.read_structure cant read the structure of a table"

    def __init__(self, database: str, table: str, message="") -> None:
        if message == "":
            message = f'In Database: "{database}" the structure of the Table: "{table}" couldnt be read'
        super().__init__(message)


class SQLMissingArgs(Exception):
    "Raised when the function self.use_sql_lang or self.sql_terminal doesnt have enough args"

    def __init__(self, exception: str, message="") -> None:
        if message == "":
            message = f'There arent enough aruments real_exception{exception}'
        super().__init__(message)

class SQLMissingSemicolon(Exception):
    "Raised when no semicolon"

    def __init__(self, message="") -> None:
        if message == "":
            message = f'Semicolon is missing'
        super().__init__(message)