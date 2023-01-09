from __future__ import annotations

from typing import Union, AnyStr


class TagOperator(str):
    """
    Class that represents a valid tag-operator for the WHERE-clause in an InfluxDB query.
    """
    def __new__(cls, operator: AnyStr) -> TagOperator:
        obj = super().__new__(cls, operator)
        obj.operator = operator
        return obj

    def __eq__(self, other: Union[TagOperator, AnyStr]):
        assert isinstance(other, (TagOperator, str)), f"'other' must be of type {TagOperator} or {str}"
        return self.operator == other

    @staticmethod
    def equal():
        """
        Returns:
            TagOperator("=")
        """
        return TagOperator("=")

    @staticmethod
    def not_equal():
        """
        Returns:
            TagOperator("!=")
        """
        return TagOperator("!=")

    @staticmethod
    def greater_than():
        """
        Returns:
            TagOperator(">")
        """
        return TagOperator(">")

    @staticmethod
    def less_than():
        """
        Returns:
            TagOperator("<")
        """
        return TagOperator("<")

    @staticmethod
    def greater_than_or_equal_to():
        """
        Returns:
            TagOperator(">=")
        """
        return TagOperator(">=")

    @staticmethod
    def less_than_or_equal_to():
        """
        Returns:
            TagOperator("<=")
        """
        return TagOperator("<=")
