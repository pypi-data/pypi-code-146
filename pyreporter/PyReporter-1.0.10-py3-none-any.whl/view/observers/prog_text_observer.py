from .observer import Observer
from ..export import ExportSubject
from ...data_frames import ExcelDf
from ...tools import DataFrameTools as DfTools
from ...events import ExcelExportEvent
from .excel_export_observer import ExcelExportObserver
from ...events.progress_event import *
import traceback
from typing import Any, Optional


# output of the progress for running the report
PROGRESS_OUTPUT_FILE = "progress_log.txt"


class ProgTextObserver(Observer):
    def __init__(self, verbose: bool = True, debug: bool = True, export_calc_tables: bool = False, progress_to_txt: bool = False):
        super().__init__()
        self._verbose = bool(verbose or debug)
        self._debug = debug
        self._export = export_calc_tables
        self._progress_to_txt = progress_to_txt

        self._step = 0
        self._excel_export_view = ExportSubject()
        self._excel_export_view.attach(ExcelExportObserver())

        # get the file to write the progress
        self._file = None
        if (self._progress_to_txt):
            with open(PROGRESS_OUTPUT_FILE, 'w+') as file_ptr:
                file_ptr.seek(0)
                file_ptr.write(f"")


    # update(): Updates the message
    def _update(self, message: str, end_with_new_line: bool = True):
        if (not end_with_new_line):
            print(message, end = "")
        else:
            print(message)

        if (self._progress_to_txt):
            with open(PROGRESS_OUTPUT_FILE, 'a+') as file_ptr:
                file_ptr.write(f"{message}\n")


    # _export_data(file_name, source_table): Export excel files containing the data
    def _export_data(self, file_name: str, source_table: pd.DataFrame) -> str:
        file = f"./debug/{file_name}.xlsx"
        source_table = DfTools.df_to_celled_df(source_table)
        self._excel_export_view.notify(ExcelExportEvent([ExcelDf(source_table)], loc = file, sheet = file_name))
        return file


    # _check_debug_event_print(out_event): Determines if the 'out_event' is
    #   ready to be print
    def _check_debug_event_print(self, out_event: DebugOutEvent) -> bool:
        return (self._verbose and not out_event.debug) or (self._debug and out_event.debug)


    # get_sql_check_msg(out_event): Retrieves the string result from checking
    #   an SQL query
    def get_sql_check_msg(self, out_event: SqlQueryCheckEvent) -> str:
        message = f"\n############### SQL Query Check ##################"
        message += f"\n\nSource Name: {out_event.source_name}"
        message += f"\nDSN: {out_event.dsn_name}"
        message += f"\n\nSQL Query: \n\n{out_event.sql_query}"
        message += f"\n\n###################################################"
        return message


    # notify_sql_check(out_event): Prints the corresponding SQL query
    def notify_sql_check(self, out_event: SqlQueryCheckEvent):
        if (self._debug):
            message = self.get_sql_check_msg(out_event)
            self._update(message)


    # get_import_msg(out_event): Retreives the string result of
    #   an imported table
    def get_import_msg(self, out_event: ImportEvent, is_export: Optional[bool] = None) -> str:
        if (is_export is None):
            is_export = bool(self._export and out_event.export_file_name is not None)

        message = f"\n@@@@@@@@@@@@@@@ Imported Data @@@@@@@@@@@@@@@@@@@@@@"
        message += f"\n\nSource Name: {out_event.name}"
        message += f"\nSource Type: {out_event.source_type.__name__}"
        message += f"\nSource Content:\n\n{out_event.source_table}"

        if (is_export):
            message += f"\n\nExported Data to \"{path}\""

        message += f"\n\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        return message


    # notify_import(out_event): Prints the corresponding imported table
    def notify_import(self, out_event: ImportEvent):
        is_export = bool(self._export and out_event.export_file_name is not None)

        # exoprt the table
        if (is_export):
            path = self._export_data(out_event.export_file_name, out_event.source_table)

        if (self._verbose):
            message = self.get_import_msg(out_event, is_export = is_export)
            self._update(message)


    # get_step_msg(out_event): Retrives the string result of an
    #   a corresponding step being run in the report
    def get_step_msg(self, out_event: StepEvent) -> str:
        message = f"======== Step {step}: {out_event.step_name} ========"
        border_message = "=" * len(message)

        message = f"\n\n\n{border_message}\n{message}\n{border_message}\n\n"
        return message


    # notify_step(): Prints out the corresponding step being run in the report
    def notify_step(self, out_event: StepEvent):
        if (self._verbose):
            # retrieve the corresponding step no.
            step = out_event.step_no
            if (out_event.step_no is None):
                self._step += 1
                step = self._step
            else:
                self._step = step

            message = self.get_step_msg(out_event)
            self._update(message)


    # get_table_check_msg(out_event, is_debug, is_export): Retrieves the string result
    #   a corresponding table
    def get_table_check_msg(self, out_event: TableCheckEvent, is_debug: Optional[bool] = None, is_export: Optional[bool] = None) -> str:
        message = ""

        if (is_debug is None):
            is_debug = bool(self._check_debug_event_print(out_event))

        if (is_export is None):
            is_export = bool(self._export and out_event.export_file_name is not None)

        if (is_debug):
            message += "\n+--------------- Table Check ------------------------+"
            message += f"\n\nTable Name: {out_event.name}"
            message += f"\nTable Content:\n\n{out_event.source_table}"

        # export the table
        if (is_export):
            message += f"\n\nExported Data to \"{path}\""

        if (is_debug):
            message += f"\n\n+----------------------------------------------------+"

        return message


    # notify_table_check(out_event): Prints out the corresponding table and exports it if needed
    def notify_table_check(self, out_event: TableCheckEvent):
        is_debug = bool(self._check_debug_event_print(out_event))
        is_export = bool(self._export and out_event.export_file_name is not None)
        message = self.get_table_check_msg(out_event, is_debug, is_export)

        # export the table
        if (is_export):
            path = self._export_data(out_event.export_file_name, out_event.source_table)

        if (is_debug):
            self._update(message)


    # get_print_msg(out_event): Retrieves the string result from a text flag
    def get_print_msg(self, out_event: PrintEvent) -> str:
        return out_event.text


    # notify_print(out_event): Prints out text flags
    def notify_print(self, out_event: PrintEvent):
        if (self._check_debug_event_print(out_event)):
            message = self.get_print_msg(out_event)
            self._update(message, end_with_new_line = out_event.end_with_new_line)


    # get_list_msg(out_event): Retrieves the string result of print a list
    def get_list_msg(self, out_event: ListPrintEvent) -> str:
        message = ""
        if (out_event.prefix is not None):
            message += f"{out_event.prefix}\n"

        if (not out_event.flatten):
            for e in out_event.lst:
                message += f"{e}\n"
        else:
            message += f"{out_event.lst}\n"

        if (out_event.suffix is not None):
            message += f"{out_event.suffix}\n"

        return message


    # notify_list(out_event): Prints out a list
    def notify_list(self, out_event: ListPrintEvent):
        if (self._check_debug_event_print(out_event)):
            message = self.get_list_msg(out_event)
            self._update(message)


    # get_err_msg(out_event): Retrieves the string result of an error
    def get_err_msg(self, out_event: ErrEvent) -> str:
        exception_lst = traceback.format_exception(type(out_event.exception), out_event.exception, out_event.exception.__traceback__)
        exception_str = ""
        border_str = f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

        for e in exception_lst:
            exception_str += e

        message = ""
        if (not out_event.no_decorator):
            message += f"\n{border_str}"
            message += f"\n!!!!!!!!!!!!!! AN ERROR HAS OCCURRED !!!!!!!!!!!!!!!!!!!!\n\n"

        message += f"Error: {type(out_event.exception).__name__}: {out_event.exception}"
        message += f"\n\nTraceback:\n{exception_str}"

        if (not out_event.no_decorator):
            message += f"\n\n{border_str}"
            message += f"\n{border_str}"

        return message


    # notify_err(out_event): Prints out the error
    def notify_err(self, out_event: ErrEvent):
        if (self._check_debug_event_print(out_event)):
            message = self.get_err_msg(out_event)
            self._update(message)


    # notify(target): Updates the observer based off 'target'
    def notify(self, target: Any):
        if (isinstance(target, SqlQueryCheckEvent)):
            self.notify_sql_check(target)

        elif (isinstance(target, ImportEvent)):
            self.notify_import(target)

        elif (isinstance(target, StepEvent)):
            self.notify_step(target)

        elif (isinstance(target, TableCheckEvent)):
            self.notify_table_check(target)

        elif (isinstance(target, PrintEvent)):
            self.notify_print(target)

        elif (isinstance(target, ListPrintEvent)):
            self.notify_list(target)

        elif (isinstance(target, ErrEvent)):
            self.notify_err(target)


    # get_str(target): Retrives the string representation of an event
    def get_str(self, target: Any) -> str:
        result = ""

        if (isinstance(target, SqlQueryCheckEvent)):
            result = self.get_sql_check_msg(target)

        elif (isinstance(target, ImportEvent)):
            result = self.get_import_msg(target)

        elif (isinstance(target, StepEvent)):
            result = self.get_step_msg(target)

        elif (isinstance(target, TableCheckEvent)):
            result = self.get_table_check_msg(target)

        elif (isinstance(target, PrintEvent)):
            result = self.get_print_msg(target)

        elif (isinstance(target, ListPrintEvent)):
            result = self.get_list_msg(target)

        elif (isinstance(target, ErrEvent)):
            result = self.get_err_msg(target)

        return result
