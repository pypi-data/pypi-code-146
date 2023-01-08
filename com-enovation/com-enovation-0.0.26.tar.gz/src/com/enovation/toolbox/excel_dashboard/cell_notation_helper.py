import re
from inspect import stack
from logging import getLogger
from re import Match

from xlsxwriter.utility import xl_cell_to_rowcol, xl_rowcol_to_cell


class CellNotationHelper:
    """
    1. get_address_pattern
    2. is_pattern_xxx
    3. is_address_xxx_pattern
    4. is_address_xxx_correct
    5. transform_xxx_into_xxx
    6. translate_xxx_to_reference

    Old test classes to reshuffle:
    - get_absolute_from_relative_address
    - transform_excel_expression
    """

    # ################################################################################################################ #
    # Fully tested in test_function__get_address_pattern                                                             # #
    # ################################################################################################################ #

    @staticmethod
    def get_address_pattern(str_address: str) -> str:
        """
        Function that analyzes an address, and returns the pattern:
        - cells: --A--1, --A-$1, --A@&1
        - range: --A--1:--A--1
        - column: --A:--A
        - row: --1:--1

        In case the address being analyzed is incorrect, an exception is raised.
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        str_the_return: str = ""

        # 1. We check the address as a cell
        _match_object: Match = re.match(
            pattern=r"^(\@?)(\$?)([A-Z]+)(\@?)(\$?)([1-9][0-9]*)$",
            string=str_address
        )
        if _match_object:

            if _match_object.group(1) == "":
                str_the_return = str_the_return + "-"
            else:
                str_the_return = str_the_return + "@"

            if _match_object.group(2) == "":
                str_the_return = str_the_return + "-"
            else:
                str_the_return = str_the_return + "$"

            str_the_return = str_the_return + "A"

            if _match_object.group(4) == "":
                str_the_return = str_the_return + "-"
            else:
                str_the_return = str_the_return + "@"

            if _match_object.group(5) == "":
                str_the_return = str_the_return + "-"
            else:
                str_the_return = str_the_return + "$"

            str_the_return = str_the_return + "1"

        else:

            # 2. We check the address as a range
            _match_object: Match = re.match(
                pattern=r"^(\@?)(\$?)([A-Z]+)(\@?)(\$?)([1-9][0-9]*):(\@?)(\$?)([A-Z]+)(\@?)(\$?)([1-9][0-9]*)$",
                string=str_address
            )
            if _match_object:
                _lst_tokens: list[str] = str_address.split(":")
                str_the_return = \
                    CellNotationHelper.get_address_pattern(str_address=_lst_tokens[0]) +\
                    ":" +\
                    CellNotationHelper.get_address_pattern(str_address=_lst_tokens[1])

            else:
                # 3. We check the address as a column: --A:--A
                _match_object: Match = re.match(
                    pattern=r"^(\@?)(\$?)([A-Z]+):(\@?)(\$?)([A-Z]+)$",
                    string=str_address
                )
                if _match_object:

                    if _match_object.group(1) == "":
                        str_the_return = str_the_return + "-"
                    else:
                        str_the_return = str_the_return + "@"

                    if _match_object.group(2) == "":
                        str_the_return = str_the_return + "-"
                    else:
                        str_the_return = str_the_return + "$"

                    str_the_return = str_the_return + "A:"

                    if _match_object.group(4) == "":
                        str_the_return = str_the_return + "-"
                    else:
                        str_the_return = str_the_return + "@"

                    if _match_object.group(5) == "":
                        str_the_return = str_the_return + "-"
                    else:
                        str_the_return = str_the_return + "$"

                    str_the_return = str_the_return + "A"

                else:

                    # 4. We check the address as a row: --1:--1
                    _match_object: Match = re.match(
                        pattern=r"^(\@?)(\$?)([1-9][0-9]*):(\@?)(\$?)([1-9][0-9]*)$",
                        string=str_address
                    )
                    if _match_object:

                        if _match_object.group(1) == "":
                            str_the_return = str_the_return + "-"
                        else:
                            str_the_return = str_the_return + "@"

                        if _match_object.group(2) == "":
                            str_the_return = str_the_return + "-"
                        else:
                            str_the_return = str_the_return + "$"

                        str_the_return = str_the_return + "1:"

                        if _match_object.group(4) == "":
                            str_the_return = str_the_return + "-"
                        else:
                            str_the_return = str_the_return + "@"

                        if _match_object.group(5) == "":
                            str_the_return = str_the_return + "-"
                        else:
                            str_the_return = str_the_return + "$"

                        str_the_return = str_the_return + "1"

                    else:
                        raise Exception(f"The address '{str_address}' is not recognized as an address, and its pattern "
                                        f"could not be determined.")

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return str_the_return

    # ################################################################################################################ #
    # Fully tested in test_function__is_pattern_xxx                                                                  # #
    # ################################################################################################################ #

    @staticmethod
    def is_pattern_correct(str_pattern: str) -> bool:
        """
        Function that returns whether the pattern is correct.

        In case the pattern is incorrect, no exception is raised, but False is returned.
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        bool_the_return: bool = False

        _match_object: Match = re.match(
            pattern=r"^(\@|-)(\$|-)A(\@|-)(\$|-)1$|"                                # Cell
                    r"^(\@|-)(\$|-)A(\@|-)(\$|-)1:(\@|-)(\$|-)A(\@|-)(\$|-)1$|"     # Range
                    r"^(\@|-)(\$|-)A:(\@|-)(\$|-)A$|"                               # Column
                    r"^(\@|-)(\$|-)1:(\@|-)(\$|-)1$",                               # Row
            string=str_pattern
        )
        if _match_object:
            bool_the_return = True

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return bool_the_return

    @staticmethod
    def is_pattern_cell(str_pattern: str) -> bool:
        """
        Function that returns whether the pattern corresponds to a cell: --A--1, --A-$1, --A@&1

        In case the pattern is incorrect, an exception is raised.
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        bool_the_return: bool = False

        if CellNotationHelper.is_pattern_correct(str_pattern=str_pattern):

            _match_object: Match = re.match(
                pattern=r"^(\@|-)(\$|-)A(\@|-)(\$|-)1$",
                string=str_pattern
            )
            if _match_object:
                bool_the_return = True

        else:
            raise Exception(f"Pattern '{str_pattern}' is incorrect, and not a cell!")

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return bool_the_return

    @staticmethod
    def is_pattern_range(str_pattern: str) -> bool:
        """
        Function that returns whether the pattern corresponds to a range: --A--1:--A--1

        In case the pattern is incorrect, an exception is raised.
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        bool_the_return: bool = False

        if CellNotationHelper.is_pattern_correct(str_pattern=str_pattern):

            _match_object: Match = re.match(
                pattern=r"^(\@|-)(\$|-)A(\@|-)(\$|-)1:(\@|-)(\$|-)A(\@|-)(\$|-)1$",
                string=str_pattern
            )
            if _match_object:
                bool_the_return = True

        else:
            raise Exception(f"Pattern '{str_pattern}' is incorrect, and not a range!")

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return bool_the_return

    @staticmethod
    def is_pattern_column(str_pattern: str) -> bool:
        """
        Function that returns whether the pattern corresponds to a column: --A:--A

        In case the pattern is incorrect, an exception is raised.
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        bool_the_return: bool = False

        if CellNotationHelper.is_pattern_correct(str_pattern=str_pattern):

            _match_object: Match = re.match(
                pattern=r"^(\@|-)(\$|-)A:(\@|-)(\$|-)A$",
                string=str_pattern
            )
            if _match_object:
                bool_the_return = True

        else:
            raise Exception(f"Pattern '{str_pattern}' is incorrect, and not a column!")

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return bool_the_return

    @staticmethod
    def is_pattern_row(str_pattern: str) -> bool:
        """
        Function that returns whether the pattern corresponds to a row: --1:--1

        In case the pattern is incorrect, an exception is raised.
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        bool_the_return: bool = False

        if CellNotationHelper.is_pattern_correct(str_pattern=str_pattern):

            _match_object: Match = re.match(
                pattern=r"^(\@|-)(\$|-)1:(\@|-)(\$|-)1$",
                string=str_pattern
            )
            if _match_object:
                bool_the_return = True

        else:
            raise Exception(f"Pattern '{str_pattern}' is incorrect, and not a row!")

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return bool_the_return

    # ################################################################################################################ #
    # Fully tested in test_function__is_address_xxx_pattern                                                          # #
    # ################################################################################################################ #

    @staticmethod
    def is_address_pattern_correct(str_address: str) -> bool:
        """
        Function that returns whether the address pattern is correct.

        In case the address is incorrect, no exception is raised, but False is returned.
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        bool_the_return: bool = False

        # noinspection PyBroadException
        try:
            CellNotationHelper.get_address_pattern(str_address=str_address)
            bool_the_return = True
        except Exception:
            pass

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return bool_the_return

    @staticmethod
    def is_address_cell_pattern(str_address: str) -> bool:
        """
        Function that returns whether the address pattern is a cell.

        In case the address is not a correct one, an exception is raised.
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        bool_the_return: bool = CellNotationHelper.is_pattern_cell(
            str_pattern=CellNotationHelper.get_address_pattern(str_address=str_address)
        )

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return bool_the_return

    @staticmethod
    def is_address_range_pattern(str_address: str) -> bool:
        """
        Function that returns whether the address pattern is a range.

        In case the address is not a correct one, an exception is raised.
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        bool_the_return: bool = CellNotationHelper.is_pattern_range(
            str_pattern=CellNotationHelper.get_address_pattern(str_address=str_address)
        )

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return bool_the_return

    @staticmethod
    def is_address_column_pattern(str_address: str) -> bool:
        """
        Function that returns whether the address pattern is a column.

        In case the address is not a correct one, an exception is raised.
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        bool_the_return: bool = CellNotationHelper.is_pattern_column(
            str_pattern=CellNotationHelper.get_address_pattern(str_address=str_address)
        )

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return bool_the_return

    @staticmethod
    def is_address_row_pattern(str_address: str) -> bool:
        """
        Function that returns whether the address pattern is a row.

        In case the address is not a correct one, an exception is raised.
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        bool_the_return: bool = CellNotationHelper.is_pattern_row(
            str_pattern=CellNotationHelper.get_address_pattern(str_address=str_address)
        )

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return bool_the_return

    # ################################################################################################################ #
    # Fully tested in test_function__is_address_xxx_correct                                                          # #
    # ################################################################################################################ #

    @staticmethod
    def is_address_correct(str_address: str) -> bool:
        """
        Function that returns whether the address is correct: both patterns and values.

        Exceptions are raised in case:
        - str_address pattern is not correct
        - str_address is dynamic
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        _bool_the_return: bool = False

        try:
            _str_the_pattern = CellNotationHelper.get_address_pattern(str_address=str_address)
        except Exception as an_exception:
            raise Exception(f"The parameter str_address '{str_address}' could not be pattern-ized.") from an_exception

        if CellNotationHelper.is_pattern_cell(str_pattern=_str_the_pattern):
            _bool_the_return = CellNotationHelper.is_address_cell_correct(str_address=str_address)
        elif CellNotationHelper.is_pattern_range(str_pattern=_str_the_pattern):
            _bool_the_return = CellNotationHelper.is_address_range_correct(str_address=str_address)
        elif CellNotationHelper.is_pattern_column(str_pattern=_str_the_pattern):
            _bool_the_return = CellNotationHelper.is_address_column_correct(str_address=str_address)
        elif CellNotationHelper.is_pattern_row(str_pattern=_str_the_pattern):
            _bool_the_return = CellNotationHelper.is_address_row_correct(str_address=str_address)
        else:
            raise Exception(f"Could not process the address '{str_address}'.")

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return _bool_the_return

    @staticmethod
    def is_address_cell_correct(str_address: str) -> bool:
        """
        Function that returns whether the address is a correct cell: no particular business rule

        Exceptions are raised in case:
        - str_address pattern is not correct
        - str_address pattern is not cell
        - str_address is dynamic
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        _bool_the_return: bool = False
        _str_the_pattern: str = ""

        # An exception is raised in case the address cannot be pattern-ized
        _str_the_pattern = CellNotationHelper.get_address_pattern(str_address=str_address)

        # In case the pattern is not a cell, we raise an exception
        if not CellNotationHelper.is_pattern_cell(str_pattern=_str_the_pattern):
            raise Exception(f"The parameter str_address '{str_address}' is not a cell.")

        # If the address is dynamic, we can't check if it is correct...
        if "@" in str_address:
            raise Exception(f"The parameter str_address '{str_address}' contains one (or more) '@', and we cannot "
                            f"confirm if it is a correct address or not. Make sure you provide address without any "
                            f"'@'.")

        # No other rule to check for cells...
        _bool_the_return = True

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return _bool_the_return

    @staticmethod
    def is_address_range_correct(str_address: str) -> bool:
        """
        Function that returns whether the address is a correct range:
        - Column 1 should be lower or equal to Column 2
        - Row 1 should be lower or equal to Row 2.

        Exceptions are raised in case:
        - str_address pattern is not correct
        - str_address pattern is not range
        - str_address is dynamic
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        _bool_the_return: bool = False
        _str_the_pattern: str = ""

        # An exception is raised in case the address cannot be pattern-ized
        _str_the_pattern = CellNotationHelper.get_address_pattern(str_address=str_address)

        # In case the pattern is not a range, we raise an exception
        if not CellNotationHelper.is_pattern_range(str_pattern=_str_the_pattern):
            raise Exception(f"The parameter str_address '{str_address}' is not a range.")

        # If the address is dynamic, we can't check if it is correct...
        if "@" in str_address:
            raise Exception(f"The parameter str_address '{str_address}' contains one (or more) '@', and we cannot "
                            f"confirm if it is a correct address or not. Make sure you provide address without any "
                            f"'@'.")

        # We remove the dollar signs, if any, and tokenize the range into 2 cells
        _lst_str_cells: list[str] = str_address.replace("$", "").split(":")

        # We compare the columns, then the rows
        _str_col_1: str = re.sub("\\d", "", _lst_str_cells[0])
        _str_col_2: str = re.sub("\\d", "", _lst_str_cells[1])

        if len(_str_col_1) < len(_str_col_2):
            _bool_the_return = True
        elif len(_str_col_1) == len(_str_col_2):
            if _str_col_1 <= _str_col_2:
                _bool_the_return = True

        if _bool_the_return:
            # For the rows, we have to compare integers, not strings
            _int_row_1: int = int(re.sub("[A-Z]", "", _lst_str_cells[0]))
            _int_row_2: int = int(re.sub("[A-Z]", "", _lst_str_cells[1]))

            if _int_row_1 <= _int_row_2:
                _bool_the_return = True

            else:
                _bool_the_return = False

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return _bool_the_return

    @staticmethod
    def is_address_column_correct(str_address: str) -> bool:
        """
        Function that returns whether the address is a correct column: column 1 should be lower or equal to Column 2.

        Exceptions are raised in case:
        - str_address pattern is not correct
        - str_address pattern is not column
        - str_address is dynamic
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        _bool_the_return: bool = False
        _str_the_pattern: str = ""

        # An exception is raised in case the address cannot be pattern-ized
        _str_the_pattern = CellNotationHelper.get_address_pattern(str_address=str_address)

        # In case the pattern is not a column, we raise an exception
        if not CellNotationHelper.is_pattern_column(str_pattern=_str_the_pattern):
            raise Exception(f"The parameter str_address '{str_address}' is not a column.")

        # If the address is dynamic, we can't check if it is correct...
        if "@" in str_address:
            raise Exception(f"The parameter str_address '{str_address}' contains one (or more) '@', and we cannot "
                            f"confirm if it is a correct address or not. Make sure you provide address without any "
                            f"'@'.")

        # We remove the dollar signs, if any, and tokenize the column range into 2 columns
        _lst_str_columns: list[str] = str_address.replace("$", "").split(":")

        # We compare the columns
        _str_col_1: str = re.sub("\\d", "", _lst_str_columns[0])
        _str_col_2: str = re.sub("\\d", "", _lst_str_columns[1])

        if len(_str_col_1) < len(_str_col_2):
            _bool_the_return = True
        elif len(_str_col_1) == len(_str_col_2):
            if _str_col_1 <= _str_col_2:
                _bool_the_return = True

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return _bool_the_return

    @staticmethod
    def is_address_row_correct(str_address: str) -> bool:
        """
        Function that returns whether the address is a correct row: row 1 should be lower or equal to row 2.

        Exceptions are raised in case:
        - str_address pattern is not correct
        - str_address pattern is not column
        - str_address is dynamic
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        _bool_the_return: bool = False
        _str_the_pattern: str = ""

        # An exception is raised in case the address cannot be pattern-ized
        _str_the_pattern = CellNotationHelper.get_address_pattern(str_address=str_address)

        # In case the pattern is not a row, we raise an exception
        if not CellNotationHelper.is_pattern_row(str_pattern=_str_the_pattern):
            raise Exception(f"The parameter str_address '{str_address}' is not a row.")

        # If the address is dynamic, we can't check if it is correct...
        if "@" in str_address:
            raise Exception(f"The parameter str_address '{str_address}' contains one (or more) '@', and we cannot "
                            f"confirm if it is a correct address or not. Make sure you provide address without any "
                            f"'@'.")

        # We remove the dollar signs, if any, and tokenize the row range into 2 row
        _lst_str_rows: list[str] = str_address.replace("$", "").split(":")

        # For the rows, we have to compare integers, not strings
        _int_row_1: int = int(re.sub("[A-Z]", "", _lst_str_rows[0]))
        _int_row_2: int = int(re.sub("[A-Z]", "", _lst_str_rows[1]))

        if _int_row_1 <= _int_row_2:
            _bool_the_return = True

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return _bool_the_return

    # ################################################################################################################ #
    # Fully tested in test_function__transform_xxx_into_xxx                                                          # #
    # ################################################################################################################ #

    @staticmethod
    def transform_address_into_tokens(
            str_address: str,
    ) -> dict:
        """
        Function that transforms a tokenized address into a string address.

        An exception is thrown in case the tokens does not have all the expected keys (either more or less).
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called with "
                                  f"str_address = '{str_address}'.")

        _dict_the_return: dict = {
            "first_col": None, "first_col_at": None, "first_col_doll": None,
            "first_row": None, "first_row_at": None, "first_row_doll": None,
            "last_col": None, "last_col_at": None, "last_col_doll": None,
            "last_row": None, "last_row_at": None, "last_row_doll": None,
        }

        # 1. We check the address as a cell
        _match_object: Match = re.match(
            pattern=r"^(\@?)(\$?)([A-Z]+)(\@?)(\$?)([1-9][0-9]*)$",
            string=str_address
        )
        if _match_object:

            _dict_the_return["first_col_at"] = (_match_object.group(1) == "@")
            _dict_the_return["first_col_doll"] = (_match_object.group(2) == "$")
            _dict_the_return["first_col"] = _match_object.group(3)

            _dict_the_return["first_row_at"] = (_match_object.group(4) == "@")
            _dict_the_return["first_row_doll"] = (_match_object.group(5) == "$")
            _dict_the_return["first_row"] = _match_object.group(6)

        else:

            # 2. We check the address as a range
            _match_object: Match = re.match(
                pattern=r"^(\@?)(\$?)([A-Z]+)(\@?)(\$?)([1-9][0-9]*):(\@?)(\$?)([A-Z]+)(\@?)(\$?)([1-9][0-9]*)$",
                string=str_address
            )
            if _match_object:

                _dict_the_return["first_col_at"] = (_match_object.group(1) == "@")
                _dict_the_return["first_col_doll"] = (_match_object.group(2) == "$")
                _dict_the_return["first_col"] = _match_object.group(3)

                _dict_the_return["first_row_at"] = (_match_object.group(4) == "@")
                _dict_the_return["first_row_doll"] = (_match_object.group(5) == "$")
                _dict_the_return["first_row"] = _match_object.group(6)

                _dict_the_return["last_col_at"] = (_match_object.group(7) == "@")
                _dict_the_return["last_col_doll"] = (_match_object.group(8) == "$")
                _dict_the_return["last_col"] = _match_object.group(9)

                _dict_the_return["last_row_at"] = (_match_object.group(10) == "@")
                _dict_the_return["last_row_doll"] = (_match_object.group(11) == "$")
                _dict_the_return["last_row"] = _match_object.group(12)

            else:
                # 3. We check the address as a column: --A:--A
                _match_object: Match = re.match(
                    pattern=r"^(\@?)(\$?)([A-Z]+):(\@?)(\$?)([A-Z]+)$",
                    string=str_address
                )
                if _match_object:

                    _dict_the_return["first_col_at"] = (_match_object.group(1) == "@")
                    _dict_the_return["first_col_doll"] = (_match_object.group(2) == "$")
                    _dict_the_return["first_col"] = _match_object.group(3)

                    _dict_the_return["last_col_at"] = (_match_object.group(4) == "@")
                    _dict_the_return["last_col_doll"] = (_match_object.group(5) == "$")
                    _dict_the_return["last_col"] = _match_object.group(6)

                else:

                    # 4. We check the address as a row: --1:--1
                    _match_object: Match = re.match(
                        pattern=r"^(\@?)(\$?)([1-9][0-9]*):(\@?)(\$?)([1-9][0-9]*)$",
                        string=str_address
                    )
                    if _match_object:

                        _dict_the_return["first_row_at"] = (_match_object.group(1) == "@")
                        _dict_the_return["first_row_doll"] = (_match_object.group(2) == "$")
                        _dict_the_return["first_row"] = _match_object.group(3)

                        _dict_the_return["last_row_at"] = (_match_object.group(4) == "@")
                        _dict_the_return["last_row_doll"] = (_match_object.group(5) == "$")
                        _dict_the_return["last_row"] = _match_object.group(6)

                    else:
                        raise Exception(f"The address '{str_address}' is not recognized as an address, and it cannot "
                                        f"be tokenized.")

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning "
                                  f"'{_dict_the_return}'.")
        return _dict_the_return

    @staticmethod
    def transform_tokens_into_address(
            dict_tokens: dict,
    ) -> str:
        """
        Function that tokenizes an address. An address could be:
        - A cell
        - A range
        - A set of columns
        - A set of rows.

        An exception is thrown in case the address is not correct
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called with "
                                  f"str_address = '{dict_tokens}'.")

        if {
            "first_col", "first_col_at", "first_col_doll",
            "first_row", "first_row_at", "first_row_doll",
            "last_col", "last_col_at", "last_col_doll",
            "last_row", "last_row_at", "last_row_doll"
        } != set(dict_tokens.keys()):
            raise Exception(f"Unexpected keys in the parameters dict_tokens.keys()='{', '.join(dict_tokens.keys())}'.")

        _str_the_return: str = ""

        # If we have a first col
        if dict_tokens["first_col"] is not None:
            if dict_tokens["first_col_at"]:
                _str_the_return += "@"
            if dict_tokens["first_col_doll"]:
                _str_the_return += "$"
            _str_the_return += dict_tokens["first_col"]

        # If we have a first row
        if dict_tokens["first_row"] is not None:
            if dict_tokens["first_row_at"]:
                _str_the_return += "@"
            if dict_tokens["first_row_doll"]:
                _str_the_return += "$"
            _str_the_return += dict_tokens["first_row"]

        if (dict_tokens["last_col"] is not None) | (dict_tokens["last_row"] is not None):
            _str_the_return += ":"

        # If we have a last col
        if dict_tokens["last_col"] is not None:
            if dict_tokens["last_col_at"]:
                _str_the_return += "@"
            if dict_tokens["last_col_doll"]:
                _str_the_return += "$"
            _str_the_return += dict_tokens["last_col"]

        # If we have a last row
        if dict_tokens["last_row"] is not None:
            if dict_tokens["last_row_at"]:
                _str_the_return += "@"
            if dict_tokens["last_row_doll"]:
                _str_the_return += "$"
            _str_the_return += dict_tokens["last_row"]

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning "
                                  f"'{_str_the_return}'.")
        return _str_the_return

    @staticmethod
    def transform_address_into_relative_and_absolute_address(
            str_address: str,
            b_first_col_at: bool = None, b_first_col_doll: bool = None,
            b_last_col_at: bool = None, b_last_col_doll: bool = None,
            b_first_row_at: bool = None, b_first_row_doll: bool = None,
            b_last_row_at: bool = None, b_last_row_doll: bool = None,
    ):
        """
        Customize an address, to set or unset the @ or $.

        Exceptions are thrown when:
        - The parameter str_address is not correct
        - Whenever we try to set an attribute which does not exist. Eg. b_first_row_at while str_address is a cell...
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        _dict_the_tokens: dict = CellNotationHelper.transform_address_into_tokens(str_address=str_address)

        if b_first_col_at is not None:
            if _dict_the_tokens["first_col"] is None:
                raise Exception(f"Trying to set first_col_at='{b_first_col_at}' for address "
                                f"'{str_address}', impossible.")
            _dict_the_tokens["first_col_at"] = b_first_col_at

        if b_first_col_doll is not None:
            if _dict_the_tokens["first_col"] is None:
                raise Exception(f"Trying to set first_col_doll='{b_first_col_doll}' for address "
                                f"'{str_address}', impossible.")
            _dict_the_tokens["first_col_doll"] = b_first_col_doll

        if b_first_row_at is not None:
            if _dict_the_tokens["first_row"] is None:
                raise Exception(f"Trying to set first_row_at='{b_first_row_at}' for address "
                                f"'{str_address}', impossible.")
            _dict_the_tokens["first_row_at"] = b_first_row_at

        if b_first_row_doll is not None:
            if _dict_the_tokens["first_row"] is None:
                raise Exception(f"Trying to set last_row_doll='{b_first_row_doll}' for address "
                                f"'{str_address}', impossible.")
            _dict_the_tokens["first_row_doll"] = b_first_row_doll

        if b_last_col_at is not None:
            if _dict_the_tokens["last_col"] is None:
                raise Exception(f"Trying to set last_col_at='{b_last_col_at}' for address "
                                f"'{str_address}', impossible.")
            _dict_the_tokens["last_col_at"] = b_last_col_at

        if b_last_col_doll is not None:
            if _dict_the_tokens["last_col"] is None:
                raise Exception(f"Trying to set last_col_doll='{b_last_col_doll}' for address "
                                f"'{str_address}', impossible.")
            _dict_the_tokens["last_col_doll"] = b_last_col_doll

        if b_last_row_at is not None:
            if _dict_the_tokens["last_row"] is None:
                raise Exception(f"Trying to set last_row_at='{b_last_row_at}' for address "
                                f"'{str_address}', impossible.")
            _dict_the_tokens["last_row_at"] = b_last_row_at

        if b_last_row_doll is not None:
            if _dict_the_tokens["last_row"] is None:
                raise Exception(f"Trying to set last_row_doll='{b_last_row_doll}' for address "
                                f"'{str_address}', impossible.")
            _dict_the_tokens["last_row_doll"] = b_last_row_doll

        _str_the_return: str = CellNotationHelper.transform_tokens_into_address(dict_tokens=_dict_the_tokens)

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning "
                                  f"'{_str_the_return}'.")
        return _str_the_return

    @staticmethod
    def transform_column_into_range_or_cell(
            str_column: str, int_first_row: int, int_last_row: int,
            b_check_correct: bool = True) -> str:
        """
        Function that returns a range from a column. When the range is one single cell, the function returns the cell.

        Example, for column "C:C" and int_first_row == int_last_row == 3, the function will not return "C3:C3" but "C3".

        Exceptions are raised in case:
        - if b_check_correct, str_column is not a column which is correct (both pattern and value, after having
            removed the "@" if any)
        - if !b_check_correct, str_column is not a column with proper pattern
        - the following condition is not respected: 0 < int_first_row <= int_last_row
        - str_address is dynamic

        TODO: call in this function transform_address_into_relative_and_absolute_address to properly set the row as
            absolute or relative....

        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        _lst_tokens: list[str] = str_column.split(":")

        if b_check_correct:
            if not CellNotationHelper.is_address_column_correct(str_address=str_column.replace("@", "")):
                raise Exception(f"The parameter str_address '{str_column}' is not a correct column.")
        else:
            if not CellNotationHelper.is_address_column_pattern(str_address=str_column):
                raise Exception(f"The parameter str_address '{str_column}' is not a column.")

        if (int_first_row <= 0) | (int_first_row > int_last_row):
            raise Exception(f"Rows indices are not correct, and should follow the following rule: "
                            f"0 < int_first_row ('{int_first_row}') <= int_last_row ('{int_last_row}')")

        # We determine whether we need to return a range or a cell
        if (int_first_row == int_last_row) & (_lst_tokens[0] == _lst_tokens[1]):
            str_the_return: str = _lst_tokens[0]+str(int_first_row)
        else:
            str_the_return: str = _lst_tokens[0]+str(int_first_row)+":"+_lst_tokens[1]+str(int_last_row)

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return str_the_return

    @staticmethod
    def transform_columns_intersect_rows_into_range_or_cell(str_columns: str, str_rows: str, b_check_correct=True) \
            -> str:
        """
        Function that returns a range from the intersection of a set of columns with a set of rows. When the range is
        one single cell, the function returns the cell.

        Example, intersection of "C:C" and "3:3" will not return "C3:C3" but "C3".

        Exceptions are raised in case:
        - if b_check_correct:
            - str_columns is not a set of columns which is correct (both pattern and value)
            - str_rows is not a set of row which is correct (both pattern and value)
            - returned range is not a range which is correct (both pattern and value)
        - if !b_check_correct:
            - str_column is not a set of columns with proper pattern
            - str_row is not a set of rows with proper pattern
            - returned range is not a range which with proper pattern
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        # Before starting, we check the columns and rows are correct
        if b_check_correct:
            if not CellNotationHelper.is_address_column_correct(str_address=str_columns):
                raise Exception(f"The parameter str_columns '{str_columns}' is not a correct set of columns.")
            if not CellNotationHelper.is_address_row_correct(str_address=str_rows):
                raise Exception(f"The parameter str_rows '{str_rows}' is not a correct set of rows.")
        else:
            if not CellNotationHelper.is_address_column_pattern(str_address=str_columns):
                raise Exception(f"The parameter str_columns '{str_columns}' does not have column pattern.")
            if not CellNotationHelper.is_address_row_pattern(str_address=str_rows):
                raise Exception(f"The parameter str_rows '{str_rows}' does not have row pattern.")

        _lst_str_columns: list[str] = str_columns.split(":")
        _lst_str_rows: list[str] = str_rows.split(":")

        _str_the_first_cell: str = _lst_str_columns[0]+_lst_str_rows[0]
        _str_the_second_cell: str = _lst_str_columns[1]+_lst_str_rows[1]

        # Particular case: we do not return A3:A3, but A3
        if _str_the_first_cell == _str_the_second_cell:
            _str_the_return: str = _str_the_first_cell

            if b_check_correct:
                if not CellNotationHelper.is_address_cell_correct(str_address=_str_the_return):
                    raise Exception(f"The returned value '{_str_the_return}' is not a correct cell.")
            else:
                if not CellNotationHelper.is_address_cell_pattern(str_address=_str_the_return):
                    raise Exception(f"The returned value '{_str_the_return}' does not have cell pattern.")

        # Else, both cells are distinct, we return a range...
        else:
            _str_the_return: str = _str_the_first_cell + ":" + _str_the_second_cell

            if b_check_correct:
                if not CellNotationHelper.is_address_range_correct(str_address=_str_the_return):
                    raise Exception(f"The returned value '{_str_the_return}' is not a correct range.")
            else:
                if not CellNotationHelper.is_address_range_pattern(str_address=_str_the_return):
                    raise Exception(f"The returned value '{_str_the_return}' does not have range pattern.")

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return _str_the_return

    # ################################################################################################################ #
    # Fully tested in test_function__translate_xxx_to_reference                                                      # #
    # ################################################################################################################ #

    @staticmethod
    def translate_address_to_reference(str_address: str, str_reference_cell: str) -> str:
        """
        Function that translates an address to a given reference. Only relative components prefixed with "@" are
        translated.

        Exceptions are raised in case:
        - str_address is not an address
        - str_reference_cell is not a cell which is correct
        - the resulting translated range is not correct
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        _str_the_return: str

        if CellNotationHelper.is_address_cell_pattern(str_address=str_address):
            _str_the_return = CellNotationHelper.translate_cell_to_reference(
                str_cell=str_address,
                str_reference_cell=str_reference_cell
            )

        elif CellNotationHelper.is_address_range_pattern(str_address=str_address):
            _str_the_return = CellNotationHelper.translate_range_to_reference(
                str_range=str_address,
                str_reference_cell=str_reference_cell
            )

        elif CellNotationHelper.is_address_column_pattern(str_address=str_address):
            _str_the_return = CellNotationHelper.translate_column_to_reference(
                str_column=str_address,
                str_reference_cell=str_reference_cell
            )

        elif CellNotationHelper.is_address_row_pattern(str_address=str_address):
            _str_the_return = CellNotationHelper.translate_row_to_reference(
                str_row=str_address,
                str_reference_cell=str_reference_cell
            )

        else:
            raise Exception(f"Unexpected case, with str_address='{str_address}' and "
                            f"str_reference_cell='{str_reference_cell}'.")

        if not CellNotationHelper.is_address_correct(str_address=_str_the_return):
            raise Exception(f"The translated address '{_str_the_return}' does not appear to be correct, "
                            f"with str_address='{str_address}' and str_reference_cell='{str_reference_cell}'.")

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return _str_the_return

    @staticmethod
    def translate_range_to_reference(str_range: str, str_reference_cell: str) -> str:
        """
        Function that translates a range to a given reference. Only relative components prefixed with "@" are
        translated.

        Exceptions are raised in case:
        - str_range is not a range with proper pattern
        - str_reference_cell is not a cell which is correct
        - the resulting translated range is not correct
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        if not CellNotationHelper.is_address_cell_correct(str_address=str_reference_cell):
            raise Exception(f"The parameter str_reference '{str_reference_cell}' is not correct.")

        if not CellNotationHelper.is_address_range_pattern(str_address=str_range):
            raise Exception(f"The parameter str_range '{str_range}' has a pattern which is not range.")

        _lst_str_tokens: list[str] = str_range.split(":")

        _str_the_return: str = CellNotationHelper.translate_cell_to_reference(
            str_cell=_lst_str_tokens[0],
            str_reference_cell=str_reference_cell
        ) + ":" + CellNotationHelper.translate_cell_to_reference(
            str_cell=_lst_str_tokens[1],
            str_reference_cell=str_reference_cell
        )

        if not CellNotationHelper.is_address_range_correct(str_address=_str_the_return):
            raise Exception(f"The translated range '{_str_the_return}' does not appear to be correct, "
                            f"with str_range='{str_range}' and str_reference_cell='{str_reference_cell}'.")

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return _str_the_return

    @staticmethod
    def translate_column_to_reference(str_column: str, str_reference_cell: str) -> str:
        """
        Function that translates a column range to a given reference. Only relative components prefixed with "@" are
        translated.

        A column range looks like "A:A", and is of the pattern: ??A---:??A---

        Exceptions are raised in case:
        - str_column is not a column range with proper pattern
        - str_reference_cell is not a cell which is correct
        - the resulting translated column range is not correct
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        if not CellNotationHelper.is_address_cell_correct(str_address=str_reference_cell):
            raise Exception(f"The parameter str_reference '{str_reference_cell}' is not correct.")

        if not CellNotationHelper.is_address_column_pattern(str_address=str_column):
            raise Exception(f"The parameter str_column '{str_column}' has a pattern which is not column range.")

        _lst_str_tokens: list[str] = str_column.split(":")

        _str_the_return: str = CellNotationHelper.translate_column_ref_to_reference(
            str_column_ref=_lst_str_tokens[0],
            str_reference_cell=str_reference_cell
        ) + ":" + CellNotationHelper.translate_column_ref_to_reference(
            str_column_ref=_lst_str_tokens[1],
            str_reference_cell=str_reference_cell
        )

        if not CellNotationHelper.is_address_column_correct(str_address=_str_the_return):
            raise Exception(f"The translated range '{_str_the_return}' does not appear to be correct, "
                            f"with str_column='{str_column}' and str_reference_cell='{str_reference_cell}'.")

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return _str_the_return

    @staticmethod
    def translate_row_to_reference(str_row: str, str_reference_cell: str) -> str:
        """
        Function that translates a row range to a given reference. Only relative components prefixed with "@" are
        translated.

        A row range looks like "1:1", and is of the pattern: ---??1:---??1

        Exceptions are raised in case:
        - str_row is not a row range with proper pattern
        - str_reference_cell is not a cell which is correct
        - the resulting translated row range is not correct
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        if not CellNotationHelper.is_address_cell_correct(str_address=str_reference_cell):
            raise Exception(f"The parameter str_reference '{str_reference_cell}' is not correct.")

        if not CellNotationHelper.is_address_row_pattern(str_address=str_row):
            raise Exception(f"The parameter str_row '{str_row}' has a pattern which is not row range.")

        _lst_str_tokens: list[str] = str_row.split(":")

        _str_the_return: str = CellNotationHelper.translate_row_ref_to_reference(
            str_row_ref=_lst_str_tokens[0],
            str_reference_cell=str_reference_cell
        ) + ":" + CellNotationHelper.translate_row_ref_to_reference(
            str_row_ref=_lst_str_tokens[1],
            str_reference_cell=str_reference_cell
        )

        if not CellNotationHelper.is_address_row_correct(str_address=_str_the_return):
            raise Exception(f"The translated range '{_str_the_return}' does not appear to be correct, "
                            f"with str_row='{str_row}' and str_reference_cell='{str_reference_cell}'.")

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return _str_the_return

    @staticmethod
    def translate_cell_to_reference(str_cell: str, str_reference_cell: str) -> str:
        """
        Function that translates a cell to a given reference. Only relative components prefixed with "@" are
        translated.

        Exceptions are raised in case:
        - str_cell does not have a correct pattern
        - str_reference_cell is not a cell which is correct
        - the resulting translated range is not correct
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        if not CellNotationHelper.is_address_cell_correct(str_address=str_reference_cell):
            raise Exception(f"The parameter str_reference '{str_reference_cell}' is not correct.")

        if not CellNotationHelper.is_address_cell_pattern(str_address=str_cell):
            raise Exception(f"The parameter str_cell '{str_cell}' does not have a cell pattern.")

        _str_the_return: str = str_cell

        # If the address is dynamic
        if "@" in str_cell:

            # We split the cell into 2, the column and the row
            _match_object: Match = re.match(
                pattern=r"^(\@?\$?[A-Z]+)(\@?\$?[1-9][0-9]*)$",
                string=str_cell
            )

            _str_the_return = CellNotationHelper.translate_column_ref_to_reference(
                str_column_ref=_match_object.group(1),
                str_reference_cell=str_reference_cell
            )+CellNotationHelper.translate_row_ref_to_reference(
                str_row_ref=_match_object.group(2),
                str_reference_cell=str_reference_cell
            )

        if not CellNotationHelper.is_address_cell_correct(str_address=_str_the_return):
            raise Exception(f"The translated range '{_str_the_return}' does not appear to be correct, "
                            f"with str_cell='{str_cell}' and str_reference_cell='{str_reference_cell}'.")

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return _str_the_return

    @staticmethod
    def translate_column_ref_to_reference(str_column_ref: str, str_reference_cell: str) -> str:
        """
        Function that translates a column ref to a given reference, only if prefixed with "@".

        A column ref is "C", but not "C:C".

        Exceptions are raised in case:
        - str_column_ref is not a correct alpha (possibly with $)
        - str_reference_cell is not a cell which is correct
        - the resulting column ref is not a correct alpha (possibly with $)
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        _str_the_return: str = str_column_ref

        if not CellNotationHelper.is_address_cell_correct(str_address=str_reference_cell):
            raise Exception(f"The parameter str_reference '{str_reference_cell}' is not correct.")

        _match_object: Match = re.match(
            pattern=r"^(\@?)(\$?)([A-Z]+)$",
            string=str_column_ref
        )
        if not _match_object:
            raise Exception(f"The parameter str_column_ref '{str_column_ref}' is not correct.")

        # In case the column reference is dynamic
        # E.g. str_column_ref="@$D" and str_reference_cell="B3"
        if "@" in str_column_ref:

            # We get "D"
            _str_the_pure_column_ref: str = re.sub(r"[@$]", "", str_column_ref)

            # We get "D1"
            _str_the_column_ref_as_cell: str = _str_the_pure_column_ref+"1"

            # We get "4" from "(1, 4)"
            _int_the_column_ref_as_col_index: int = xl_cell_to_rowcol(cell_str=_str_the_column_ref_as_cell)[1]

            # We get "2" from "(3, 2)"
            _int_the_reference_cell_as_col_index: int = xl_cell_to_rowcol(cell_str=str_reference_cell)[1]

            # We get "F1"
            _str_the_translated_cell = xl_rowcol_to_cell(
                row=1,
                col=_int_the_column_ref_as_col_index+_int_the_reference_cell_as_col_index
            )

            # We get "F"
            _str_the_translated_column_ref = re.sub("[0-9]", "", _str_the_translated_cell)

            # We get $F
            if "$" in str_column_ref:
                _str_the_return = "$"+_str_the_translated_column_ref
            else:
                _str_the_return = _str_the_translated_column_ref

        _match_object: Match = re.match(
            pattern=r"^(\@?)(\$?)([A-Z]+)$",
            string=_str_the_return
        )
        if not _match_object:
            raise Exception(f"The resulting column_ref '{_str_the_return}' is not correct. It was computed from "
                            f"the parameters str_column_ref='{str_column_ref}' and "
                            f"str_reference_cell='{str_reference_cell}'.")

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return _str_the_return

    @staticmethod
    def translate_row_ref_to_reference(str_row_ref: str, str_reference_cell: str) -> str:
        """
        Function that translates a row reference to a given reference, only if prefixed with "@".

        A row ref is "1", but not "1:1".

        Exceptions are raised in case:
        - str_row_ref is not a correct numeric (possibly with $)
        - str_reference_cell is not a cell which is correct
        - the resulting row ref is not a correct numeric (possibly with $)
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        _str_the_return: str = str_row_ref

        if not CellNotationHelper.is_address_cell_correct(str_address=str_reference_cell):
            raise Exception(f"The parameter str_reference '{str_reference_cell}' is not correct.")

        _match_object: Match = re.match(
            pattern=r"^(\@?)(\$?)([1-9][0-9]*)$",
            string=str_row_ref
        )
        if not _match_object:
            raise Exception(f"The parameter str_row_ref '{str_row_ref}' is not correct.")

        # In case the row reference is dynamic
        # E.g. str_row_ref="@$3" and str_reference_cell="B3"
        if "@" in str_row_ref:

            # We get "3" as a numeric
            _int_the_row_ref: int = int(re.sub(r"[@$]", "", str_row_ref))

            # We get "3" from "(3, 2)"
            _int_the_reference_cell_as_row_index: int = xl_cell_to_rowcol(cell_str=str_reference_cell)[0]

            # We get $F
            if "$" in str_row_ref:
                _str_the_return = "$"+str(_int_the_reference_cell_as_row_index+_int_the_row_ref)
            else:
                _str_the_return = str(_int_the_reference_cell_as_row_index+_int_the_row_ref)

        _match_object: Match = re.match(
            pattern=r"^(\@?)(\$?)([1-9][0-9]*)$",
            string=_str_the_return
        )
        if not _match_object:
            raise Exception(f"The resulting row_ref '{_str_the_return}' is not correct. It was computed from "
                            f"the parameters str_row_ref='{str_row_ref}' and "
                            f"str_reference_cell='{str_reference_cell}'.")

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return _str_the_return

    # ################################################################################################################ #
    # Not tested yet                                                                  # #
    # ################################################################################################################ #

    @staticmethod
    def translate_formula_to_reference(str_reference_address: str, str_formula: str) -> str:
        """
        Function that translates a formula to a given reference, only if it contains addresses prefixed with "@".

        Exceptions are raised in case:
        - str_formula cannot be successfully parsed
        - translated references are not correct
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        str_the_return: str = ""

        # We tokenize the expression, to isolate the "string" tokens to ignore
        _lst_the_expression_tokens: list[str] = CellNotationHelper._translate_formula_to_reference__tokenize(
            str_formula=str_formula
        )

        # For each token
        for str_i_token in _lst_the_expression_tokens:

            # if it starts with ["], it means the token is a string parameter, not to be processed
            if str_i_token.startswith('"'):
                str_the_return = str_the_return + str_i_token

            # else, the token is not a string
            else:

                # 1. We process cells references of the kind "A3"
                str_i_transformed_token: str = CellNotationHelper._translate_formula_to_reference__pattern_a1(
                    str_reference_address=str_reference_address,
                    str_formula_token=str_i_token
                )

                # 2. We process cells references of the kind "A:A"
                str_i_transformed_token = CellNotationHelper._translate_formula_to_reference__pattern_aa(
                    str_reference_address=str_reference_address,
                    str_formula_token=str_i_transformed_token
                )

                # 3. We process cells references of the kind "1:1"
                str_i_transformed_token = CellNotationHelper._translate_formula_to_reference__pattern_11(
                    str_reference_address=str_reference_address,
                    str_formula_token=str_i_transformed_token
                )

                # 4. Eventually, we concatenate
                str_the_return = str_the_return + str_i_transformed_token

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

        return str_the_return

    @staticmethod
    def _translate_formula_to_reference__tokenize(str_formula: str) -> list[str]:
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")
        _lst_the_return: list[str] = re.split(
            pattern=r'("(?:""|[^"])*")',
            string=str_formula
        )

        # We check the concatenation of the tokens is effectively equal to the
        # initial expression
        if str_formula != "". join(_lst_the_return):
            raise Exception(
                f"When calling function re.split(r'(\"(?:(?:\"\")|(?:[^\"]))*\")', '{str_formula}'), we obtained "
                f"a list of tokens '{', '.join(_lst_the_return)}', concatenating in a string "
                f"'{''. join(_lst_the_return)}' which is not equal to the initial expression."
            )
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

        return _lst_the_return

    @staticmethod
    def _translate_formula_to_reference__pattern_a1(str_reference_address: str, str_formula_token: str) -> str:
        """
        The regular expression is long and can be split as below:
        - (?<!\\[)\\@: matches special character "@" if not preceded by "[": this notation can be used in formulas in
          tables, and should not be altered
        - The first half of the regex, up to the "|", will match reference such as: @A1
        - The second half of the regex, from the "|", will match reference such as: A@1
        - we use "[1-9][0-9]*" rather then "\\d+", as we cannot have a cell reference which is A0

        :param str_reference_address:
        :param str_formula_token:
        :return:
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        _lst_str_cell_references: list[str] = re.findall(
            pattern=r"(?<!\[)\@\$?[A-Z]+\@?\$?[1-9][0-9]*|(?<!\[)\@?\$?[A-Z]+\@\$?[1-9][0-9]*",
            string=str_formula_token
        )

        str_the_return: str = str_formula_token

        for str_i_cell_ref in _lst_str_cell_references:
            _str_transformed_cell_ref: str = CellNotationHelper.translate_cell_to_reference(
                str_reference_cell=str_reference_address,
                str_cell=str_i_cell_ref
            )
            str_the_return = str_the_return.replace(str_i_cell_ref, _str_transformed_cell_ref, 1)

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return str_the_return

    @staticmethod
    def _translate_formula_to_reference__pattern_aa(str_reference_address: str, str_formula_token: str) -> str:
        """
        The regular expression is long and can be split as below:
        - (?<!|\\[)|\\@: matches special character "@" if not preceded by "[": this notation can be used in formulas in
          tables, and should not be altered
        - The first half of the regex, up to the "|", will match reference such as: @A:A
        - The second half of the regex, from the "|", will match reference such as: A:@A

        :param str_reference_address:
        :param str_formula_token:
        :return:
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        _lst_str_cell_references: list[str] = re.findall(
            pattern=r"(?<!\[)\@\$?[A-Z]+:\@?\$?[A-Z]+|(?<!\[)\@?\$?[A-Z]+:\@\$?[A-Z]+",
            string=str_formula_token
        )

        str_the_return: str = str_formula_token

        for str_i_column_ref in _lst_str_cell_references:
            _str_transformed_column_ref: str = CellNotationHelper.translate_column_to_reference(
                str_reference_cell=str_reference_address,
                str_column=str_i_column_ref
            )
            str_the_return = str_the_return.replace(str_i_column_ref, _str_transformed_column_ref, 1)

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return str_the_return

    @staticmethod
    def _translate_formula_to_reference__pattern_11(str_reference_address: str, str_formula_token: str) -> str:
        """
        The regular expression is long and can be split as below:
        - (?<!\\[)\\@: matches special character "@" if not preceded by "[": this notation can be used in formulas in
          tables, and should not be altered
        - The first half of the regex, up to the "|", will match reference such as: @1:1
        - The second half of the regex, from the "|", will match reference such as: 1:@1

        :param str_reference_address:
        :param str_formula_token:
        :return:
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        _lst_str_cell_references: list[str] = re.findall(
            pattern=r"(?<!\[)\@\$?[1-9][0-9]*:\@?\$?[1-9][0-9]*|(?<!\[)\@?\$?[1-9][0-9]*:\@\$?[1-9][0-9]*",
            # pattern=r"\@\$?[1-9][0-9]*:\@?\$?[1-9][0-9]*|\@?\$?[1-9][0-9]*:\@\$?[1-9][0-9]*",
            string=str_formula_token
        )

        str_the_return: str = str_formula_token

        for str_i_row_ref in _lst_str_cell_references:
            _str_transformed_row_ref: str = CellNotationHelper.translate_row_to_reference(
                str_reference_cell=str_reference_address,
                str_row=str_i_row_ref
            )
            str_the_return = str_the_return.replace(str_i_row_ref, _str_transformed_row_ref, 1)

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return str_the_return

    # @staticmethod
    # def get_absolute_from_relative_address(str_reference_address: str, str_relative_address: str) -> str:
    #     """
    #     Function that translate an address or a range, relatively to a set reference. Only the row/ column prefixed
    #     with an @ is translated.
    #
    #     Illustration:
    #     - Relative to a reference of "B3"
    #     - A relative address of "@C@5" is translated to "D7"
    #     - A relative range of "@$C@$5:D8" is translated to "$D$7:D8"
    #     - A relative range of "@C" or "@C:@D" is translated to "D" or "D:E
    #     - A relative range of "@5" or "@5:@6" is translated to "7" or "7:8"
    #
    #     :param str_reference_address: the address against which the relative addressed is expressed
    #     :param str_relative_address: the address relative to the reference
    #     :return: the address relative to the sheet
    #     """
    #     getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")
    #     _str_the_return: str = ""
    #
    #     # If the relative address is a a range, we have to process tokens one by one
    #     if ":" in str_relative_address:
    #
    #         # We recursively call the function on each token
    #         _lst_cells: list[str] = str_relative_address.split(":")
    #         _str_cell_0: str = CellNotationHelper.get_absolute_from_relative_address(
    #             str_reference_address=str_reference_address,
    #             str_relative_address=_lst_cells[0]
    #         )
    #         _str_cell_1: str = CellNotationHelper.get_absolute_from_relative_address(
    #             str_reference_address=str_reference_address,
    #             str_relative_address=_lst_cells[1]
    #         )
    #         _str_the_return = _str_cell_0 + ":" + _str_cell_1
    #
    #     # Else, the relative address is a cell, an entire column or an entire row
    #     else:
    #
    #         # We prepare the return value, removing the special character "@"
    #         _str_the_return = str_relative_address.replace("@", "")
    #
    #         # If the address contains an alpha column
    #         _match_the_column: Match = re.search(r"^@?\$?[A-Z]+", str_relative_address)
    #         if _match_the_column is not None:
    #
    #             # We get the alpha column from the address, possibly with @ and $
    #             _str_the_column: str = _match_the_column.group(0)
    #
    #             # If this alpha column is relative, aka contains an @
    #             if "@" in _str_the_column:
    #
    #                 # We get the alpha column only, excluding all other characters
    #                 _str_the_alpha: str = re.search(r"[A-Z]+$", _str_the_column).group(0)
    #
    #                 _int_the_relative_col: int = xl_cell_to_rowcol(_str_the_alpha + "1")[1]
    #                 _int_the_reference_col: int = xl_cell_to_rowcol(str_reference_address)[1]
    #
    #                 _str_the_new_alpha: str = xl_col_to_name(_int_the_relative_col + _int_the_reference_col)
    #                 _str_the_return: str = _str_the_return.replace(_str_the_alpha, _str_the_new_alpha)
    #
    #         # If the address contains an numeric row
    #         _match_the_row: Match = re.search(r"@?\$?[0-9]+$", str_relative_address)
    #         if _match_the_row is not None:
    #
    #             # We get the numeric row from the address, possibly with @ and $
    #             _str_the_row: str = _match_the_row.group(0)
    #
    #             # If this numeric row is relative, aka contains an @
    #             if "@" in _str_the_row:
    #
    #                 # We get the numeric row only, excluding all other characters
    #                 _int_the_row: int = int(re.search(r"[0-9]+$", _str_the_row).group(0))
    #
    #                 _int_the_reference_row: int = xl_cell_to_rowcol(str_reference_address)[0]
    #
    #                 _int_the_new_numerics: int = _int_the_row + _int_the_reference_row
    #                 _str_the_return: str = _str_the_return.replace(str(_int_the_row), str(_int_the_new_numerics))
    #
    #     getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
    #     return _str_the_return
