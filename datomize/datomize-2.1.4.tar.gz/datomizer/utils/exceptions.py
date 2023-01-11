class TableNotFound(Exception):
    """Raised when there is an invalid table name"""
    pass


class ColumnNotFound(Exception):
    """Raised when there is an invalid column name"""
    pass


class InvalidResponse(Exception):
    """Raised when there is an invalid column name"""
    def __init__(self, response, error_message):
        super().__init__(f"{response.text} \n {error_message}")
