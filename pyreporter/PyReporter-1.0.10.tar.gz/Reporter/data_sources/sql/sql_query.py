import enum
from .logical import And, Or, Not, Comma, Operator
from .sql_join import SqlJoin
from typing import List, Union, Optional


SQL_ALL = "*"


# SqlActionType: Types of functions for an sql query
class SqlActionType(enum.Enum):
    """
    Types of functions for an SQL query
    """

    Select = "SELECT"
    """
    Selects data to be read
    """

    Insert = "INSERT"
    """
    Inserts data to the server
    """

    Delete = "DELETE"
    """
    Deletes data from the server
    """

    Update = "UPDATE"
    """
    Updates the values for data of the server
    """


# SqlQuery: Class to parse an sql query
class SqlQuery():
    """
    A class to construct an SQL query

    Attributes
    ----------
    action: :class:`~Reporter.data_sources.sql.sql_query.SqlActionType`
        the type of action we want to perform with the query

    selection: Union[:class:`str`, List[:class:`str`]]
        the columns or entries we want to select

    location: :class:`str`
        the name of the target source table

    join: List[Union[:class:`str`, :class:`~Reporter.data_sources.sql_join.SqlJoin`]]
        The list of joins we want to perform on the source table

        **Default**: []

    condition: Optional[Union[:class:`str`, :class:`~Reporter.data_sources.sql.logical.Operator`]]
        the specific conditions for the action we want to perform

        **Default**: ``None``
    """
    def __init__(self, action: SqlActionType, selection: Union[str, List[str]], location: str, join: List[Union[str, SqlJoin]] = [], condition: Optional[Union[str, Operator]] = None):
        self.action = action
        self.selection = selection
        self.location = location
        self.join = join
        self.condition = condition


    # parse(): Parses the sql query to be used
    def parse(self) -> str:
        """
        Retrieves the string representation of the SQL query

        Returns
        -------
        :class:`str`
            The string representation of the SQL query
        """

        result = ""

        # retrieve the selection
        selection = self.selection
        if (isinstance(self.selection, List)):
            selection = Comma(self.selection).parse_sql()

        # retrieve the join needed
        join = ""
        if (self.join):
            for j in self.join:
                if (isinstance(j, SqlJoin)):
                    join += f"\n{j.parse()}"

        # retrieve the condition needed
        condition = self.condition
        if (isinstance(self.condition, Operator)):
            condition = self.condition.parse_sql()

        if (condition is not None):
            condition = f"\nWHERE {condition}"
        else:
            condition = ""

        if (self.action == SqlActionType.Select):
            result += f"{self.action.value} {selection}\nFROM {self.location}{join}{condition};"

        return result
