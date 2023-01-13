from typing import List, Union


# Operator: class for an operator for sql
# Requires: 'params' is either:
#               - str
#               - Operator
class Operator():
    """
    A class for an operator for an SQL query

    Attributes
    ----------
    params: List[Union[:class:`str`, :class:`~Reporter.data_sources.sql.logical.Operator`]]
        the parameters of the operator
    """
    def __init__(self, params):
        self.params = params


    # parse_sql: parses the logical operation to be used in sql
    def parse_sql(self) -> str:
        """
        parses the operation of the operator in an SQL query

        Returns
        -------
        :class:`str`
        """
        pass


# BinaryOP: An operator that takes in 2 or more parameters
# Requires: 'params' has 2 or more elements
class BinaryOP(Operator):
    """
    This Class inherits from :class:`~Reporter.data_sources.sql.logical.Operator`

    A class for an operator for an SQL query that takes in 2 parameters

    Attributes
    ----------
    params: List[Union[:class:`~Reporter.data_sources.sql.logical.Operator`, :class:`str`]]
        the parameters of the binary operator.

        The list for this parameter has at least 2 elements

    sql_name: :class:`str`
        The name of the operator in SQL

    with_brackets: :class:`bool`
        whether we want to use brackets to distinguish precedence for the operator

        **Default**: `True`
    """
    def __init__(self, params: List[Union[Operator, str]], sql_name: str, with_brackets: bool = True):
        super().__init__(params)
        self.sql_name = sql_name
        self.with_brackets = with_brackets


    # parse_sql: parses the logical operation to be used in sql
    def parse_sql(self) -> str:
        added_op = False
        result = ""

        if (self.with_brackets):
            result += "("

        for p in self.params:
            if (added_op):
                result += f" {self.sql_name} "
            else:
                added_op = True

            if (isinstance(p, str)):
                result += p
            else:
                result += p.parse_sql()

        if (self.with_brackets):
            result += ")"
        return result


# UnaryOP: An operator that takes in 1 parameter
# Requires: 'params' has at least 1 element
class UnaryOP(Operator):
    """
    This Class inherits from :class:`~Reporter.data_sources.sql.logical.Operator`

    A class for an operator for an SQL query that takes in 1 parameter

    Attributes
    ----------
    param: Union[:class:`~Reporter.data_sources.sql.logical.Operator`, :class:`str`]
        The parameter for the unary operator

    sql_name: :class:`str`
        The name of the operator in SQL
    """
    def __init__(self, param: Union[Operator, str], sql_name: str):
        super().__init__([param])
        self.sql_name = sql_name


    # parse_sql: parses the logical operation to be used in sql
    def parse_sql(self) -> str:
        result = f"({self.sql_name} "
        target_element = self.params[0]

        if (isinstance(target_element, str)):
            result += target_element
        else:
            result += target_element.parse_sql()

        result += ")"
        return result


# And: AND operator used for sql
class And(BinaryOP):
    """
    The "AND" operator for SQL

    Attributes
    ----------
    params: List[Union[:class:`~Reporter.data_sources.sql.logical.Operator`, :class:`str`]]
        the parameters of the "AND" operator.

        The list for this parameter has at least 2 elements
    """
    def __init__(self, params: List[Union[Operator, str]]):
        super().__init__(params, "AND")


# Or: Or operator used for sql
class Or(BinaryOP):
    """
    The "OR" operator for SQL

    Attributes
    ----------
    params: List[Union[:class:`~Reporter.data_sources.sql.logical.Operator`, :class:`str`]]
        the parameters of the "OR" operator.

        The list for this parameter has at least 2 elements
    """
    def __init__(self, params: List[Union[Operator, str]]):
        super().__init__(params, "OR")


# Not: Not operator used for sql
class Not(UnaryOP):
    """
    The "NOT" operator for SQL

    Attributes
    ----------
    params: Union[:class:`~Reporter.data_sources.sql.logical.Operator`, :class:`str`]
        the parameter of the "NOT" operator.
    """
    def __init__(self, params: Union[Operator, str]):
        super().__init__(params, "NOT")


# Comma: Used for list of items in sql
class Comma(BinaryOP):
    """
    An operator for the comma to seperate multiple items in SQL

    Attributes
    ----------
    params: List[:class:`str`]
        the parameters of the operator

        The list for this parameter has at least 2 elements
    """
    def __init__(self, params: List[str]):
        super().__init__(params, ",", with_brackets = False)
