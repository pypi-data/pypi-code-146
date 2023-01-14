from . import _Table


class Aggregate:
    """Base class for aggregate functions"""
    function = "???"

    def __init__(self, field_name: str):
        self.field_name = field_name
        self.field = None
        self.table = None

    @property
    def is_ready(self) -> bool:
        return (self.field is not None) and (self.table is not None)

    def compile(self, table: '_Table.Table') -> '_Table.CalculatedField':
        self.table = table
        self.field = table.field_by_name(self.field_name)
        return _Table.CalculatedField(self.field, self.function)


class COUNT(Aggregate):
    """COUNT aggregate function"""
    function = "COUNT"


class AVG(Aggregate):
    """AVG aggregate function"""
    function = "AVG"


class SUM(Aggregate):
    """SUM aggregate funtcion"""
    function = "SUM"


class MIN(Aggregate):
    """MIN aggregate function"""
    function = "MIN"


class MAX(Aggregate):
    """MAX aggregate function"""
    function = "MAX"