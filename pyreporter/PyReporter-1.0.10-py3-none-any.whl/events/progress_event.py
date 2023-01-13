import pandas as pd
from .out_event import OutEvent
from typing import List, Optional, Any


# DebugOutEvent: Event that has option to be used in debug mode or not
class DebugOutEvent(OutEvent):
    """
    This Class inherits from :class:`~Reporter.event.out_event.OutEvent`

    An event that has an option to be used in debug mode or not

    Attributes
    ----------
    debug: :class:`bool`
        Flag to tell whether the event is in debug mode or not

        **Default**: ``False``
    """
    def __init__(self, debug: bool = False):
        self.debug = debug


# SqlQueryCheckEvent: Event to output an SQL source's SQL query
class SqlQueryCheckEvent(OutEvent):
    """
    This Class inherits from :class:`~Reporter.event.out_event.OutEvent`

    An event that outputs the string of the SQL query that will be executed

    Attributes
    ----------
    source_name: :class:`str`
        the name of the source that executes the SQL query

    dsn_name: :class:`str`
        the name of the dsn that executes the SQL query

    sql_query: :class:`str`
        The query to be executed
    """
    def __init__(self, source_name: str, dsn_name: str, sql_query: str):
        self.source_name = source_name
        self.dsn_name = dsn_name
        self.sql_query = sql_query


# ImportEvent: Event to output imported data
class ImportEvent(OutEvent):
    """
    This Class inherits from :class:`~Reporter.event.out_event.OutEvent`

    An event to print out the imported table from a certain source

    Attributes
    ----------
    source_name: :class:`str`
        The name of the source being imported

    source_type: :class:`str`
        The name of the type of source being imported

    source_table: `DataFrame`_
        The table that is imported

    export_file_name: Optional[:class:`str`]
        the name of the file to export the table

        When this parameter is set to ``None``, then the table will not be exported.
        If a name is specified, then the table will be exported

        **Default**: ``None``
    """
    def __init__(self, source_name: str, source_type: str, source_table: pd.DataFrame, export_file_name: Optional[str] = None):
        self.name = source_name
        self.source_type = source_type
        self.source_table = source_table
        self.export_file_name = export_file_name


# StepEvent: Event to output the current step being run in the report
class StepEvent(OutEvent):
    def __init__(self, step_name: str, step_no: Optional[int] = None):
        self.step_name = step_name
        self.step_no = step_no


# TableCheckEvent: Event to check the look of a certain table
class TableCheckEvent(DebugOutEvent):
    """
    This Class inherits from :class:`~Reporter.event.progress_event.DebugOutEvent`

    An event to print out the state of a table

    Attributes
    ----------
    table_name: :class:`str`
        The name of the table

    source_table: `DataFrame`_
        The source data of the table

    export_file_name: Optional[:class:`str`]
        the name of the file to export the table, if chosen to export the table

        When this parameter is set to ``None``, then the table will not be exported.
        If a name is specified, then the table will only be exported if the ``debug`` parameter is ``True``

        **Default**: ``None``

    debug: :class:`bool`
        Whether this event is being used in debug mode or not

        **Default**: ``False``
    """
    def __init__(self, table_name: str, source_table: pd.DataFrame, export_file_name: Optional[str] = None, debug: bool = False):
        super().__init__(debug)
        self.name = table_name
        self.source_table = source_table
        self.export_file_name = export_file_name


# PrintEvent: Event to print out text
class PrintEvent(DebugOutEvent):
    """
    This Class inherits from :class:`~Reporter.event.progress_event.DebugOutEvent`

    An event to print out text

    Attributes
    ----------
    text: :class:`str`
        The text to be printed

    debug: :class:`str`
        Whether this event is being used in debug mode or not

        **Default**: False

    end_with_new_line: :class:`bool`
        Whether we want our text to end with a new line character

        **Default**: True
    """
    def __init__(self, text: str, debug: bool = False, end_with_new_line: bool = True):
        super().__init__(debug)
        self.text = text
        self.end_with_new_line = end_with_new_line


# ListPrintEvent: Event to print out a list
class ListPrintEvent(DebugOutEvent):
    """
    This Class inherits from :class:`~Reporter.event.progress_event.DebugOutEvent`

    Attributes
    ----------
    lst: List[Any]
        The list to be printed

    flatten: :class:`bool`
        whether we want to simply print the entire list instead of each individual element of the list

        **Default**: False

    debug: :class:`debug`
        Whether this event is being used in debug mode or not

        **Default**: False

    prefix: Optional[:class:`str`]
        The prefix string to print before printing the list

        **Default**: ``None``

    suffix: Optional[:class:`str`]
        The suffix string to print before printing the list

        **Default**: ``None``
    """
    def __init__(self, lst: List[Any], flatten: bool = False, debug: bool = False, prefix: Optional[str] = None, suffix: Optional[str] = None):
        super().__init__(debug)
        self.lst = lst
        self.flatten = flatten
        self.prefix = prefix
        self.suffix = suffix


# ErrEvent: Event to print when there is an error
class ErrEvent(DebugOutEvent):
    """
    This Class inherits from :class:`~Reporter.event.progress_event.DebugOutEvent`

    An event for printing out error message when an exception occurs

    Attributes
    ----------
    exception: :class:`BaseException`
        The exception that was thrown

    no_decorator: :class:`bool`
        Whether we want the prefix/suffix decorator to surround the error message

        **Default**: ``False``

    debug: :class:`str`
        Whether this event is being used in debug mode or not

        **Default**: False
    """
    def __init__(self, exception: BaseException, no_decorator: bool = False, debug: bool = False):
        super().__init__()
        self.exception = exception
        self.no_decorator = no_decorator
        self.debug = debug
