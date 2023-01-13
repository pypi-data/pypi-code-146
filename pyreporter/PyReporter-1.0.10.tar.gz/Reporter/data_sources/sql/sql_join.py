import enum
from .logical import And, Or, Not, Comma, Operator
from typing import List, Union, Optional


# SqlJoinType: Types of joining
class SqlJoinType(enum.Enum):
    """
    An Enumeration for Different types of joining for an SQL query
    """

    InnerJoin = "INNER JOIN"
    """
    Inner Join
    """

    LeftOuterJoin = "LEFT JOIN"
    """
    Left Outer Join
    """

    RightOuterJoin = "RIGHT JOIN"
    """
    Right Outer Join
    """

    OuterJoin = "FULL OUTER JOIN"
    """
    Outer Join
    """


# SqlJoin: Class to deal with joining in sql
class SqlJoin():
    """
    A class dealing with joining in SQL

    Attributes
    ----------
    join_type: :class:`~Reporter.data_sources.sql.sql_join.SqlJoinType`
        The type of join for joining

    table: :class:`str`
        The name of the table that will be joined to the source table

    condition: Union[:class:`str`, :class:`~Reporter.data_sources.sql.logical.Operator`]
        the conditions for joining the two tables
    """
    def __init__(self, join_type: SqlJoinType, table: str, condition: Union[str, Operator]):
        self.join_type = join_type
        self.table = table
        self.condition = condition

    # parse(): Parses the string representation of the join query
    def parse(self) -> str:
        """
        Retrieves the string representation of the join query

        Returns
        -------
        :class:`str`
            the string representatin of the join query
        """
        condition = self.condition
        if (isinstance(self.condition, Operator)):
            condition = self.condition.parse_sql()

        return f"{self.join_type.value} {self.table} ON {condition}"
