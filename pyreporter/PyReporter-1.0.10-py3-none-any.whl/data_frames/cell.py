from typing import Any, Optional


# Cell: Object for each cell in a dataframe
class Cell():
    """
    An object to contain extra metadata for each cell in a dataframe

    .. container:: operations

        **Supported Operations:**

        .. describe:: str(x)

            Retrieves the string representation for ``str(x.value)``

        .. describe:: x * y

            Multiplies ``x.value`` with ``y.value``

    Attributes
    ----------
    value: Any
        The data value of the cell

    excel_formula: Optional[:class:`str`]
        Any excel formulas associated with the particular cell

        **Default**: ``None``
    """
    def __init__(self, value: Any, excel_formula: Optional[str] = None):
        self.value = value
        self.excel_formula = excel_formula


    def __str__(self) -> str:
        return str(self.value)


    def __mul__(self, other: Any):
        return self.value * other


    def __rmul__(self, other: Any):
        return other * self.value


    # get_display(): Retrieves the value to be displayed
    def get_display(self) -> Any:
        """
        Retrieves the value that will be displayed for cell

        Returns
        -------
        Any
            Returns either the raw value of the cell or the cell's excel formula
        """
        if (self.excel_formula is None):
            return self.value
        else:
            return self.excel_formula
