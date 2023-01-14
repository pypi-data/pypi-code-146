class TableNotFound(Exception):
    def __init__(self, tablename: str, basename: str):
        super().__init__(f'table {tablename} is not in {basename} database')


class TableAlreadyExists(Exception):
    def __init__(self, tablename: str, basename: str):
        super().__init__(f'table {tablename} already exists in {basename} database')

class TableIsNotReal(Exception):
    def __init__(self, tablename: str):
        super().__init__(f'table {tablename} is not real, but only Real tables are supported')