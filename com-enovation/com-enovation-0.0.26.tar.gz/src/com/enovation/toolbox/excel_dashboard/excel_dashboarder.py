from datetime import datetime
from inspect import stack
from logging import Logger, getLogger
from os.path import isfile
from pathlib import Path
from typing import Optional, Type

from pandas import ExcelWriter
from xlsxwriter import Workbook
from xlsxwriter.format import Format
from xlsxwriter.worksheet import Worksheet

from com.enovation.toolbox.excel_dashboard.config_checker import ConfigChecker
from com.enovation.toolbox.excel_dashboard.widgets.widget import Widget


class ExcelDashboarder:
    """
    Class that dynamically produce advanced Excel Dashboards.
    """

    const_str__sub_directory_for_widgets: str = "widgets"

    const_str__config_label__str_worksheet_hide: str = "worksheet.hide"
    const_str__config_label__str_widgets: str = "widgets"
    const_str__config_label__str_format: str = "format"
    const_str__config_label__str_sheets: str = "sheets"

    const_str__config_label__str_address: str = "address"
    const_str__config_label__str_parameters_map: str = "parameters_map"
    const_str__config_label__str_config: str = "config"

    const_str__config_label__str_vba: str = "vba"
    const_str__config_label__str_add_vba_project: str = "workbook.add_vba_project"
    const_str__config_label__str_wb_set_vba_name: str = "workbook.set_vba_name"
    const_str__config_label__str_ws_set_vba_name: str = "worksheet.set_vba_name"

    const_str__config_label__str_ws_freeze_panes: str = "worksheet.freeze_panes"

    const_str__config_label__str_wb_set_properties: str = "workbook.set_properties"

    const_str__config_label__str_ws_set_column: str = "worksheet.set_column"

    _logger: Logger = getLogger(__name__)

    # This is the repository of all the registered widgets:
    # - The ones proposed by com.enovation packaging
    # - Along with the custom ones that are provided while instantiating the ExcelDashboarder.
    # It is structured as a dictionary:
    # - Key: the widget id (aka "$id" from the json schema)
    # - Value: the widget class
    _dict_widgets_repository: dict[str, Type[Widget]] = None

    # That is the config checker. It contains all json formats:
    # - From low level formats, listed in the class ConfigChecker. Illustration: xlsxwriter functions
    # - To com.enovation widgets, registered in the __init__, and expected to be found in the 'widgets' sub-directory.
    #   Illustration: WidgetTable
    # - To custom widgets, that are to be registered while instantiating the ExcelDashboarder
    _obj_config_checker: ConfigChecker = None

    def __init__(
            self,
            lst_custom_widgets: list[Type[Widget]] = None
    ):
        """
        Subscribe all the widgets, and instantiate the configuration checker.
        This list of widgets can be extended through the parameter lst_widgets.
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        Widget.reinitialize_default_formats()

        if lst_custom_widgets is None:
            lst_custom_widgets = []

        # We consolidate the full list of widgets:
        # - The default ones provided by com.enovation, and to be dynamically found under sub-directory "widgets"
        # - Along with the custom ones, provided through the parameter "lst_custom_widgets"
        self._dict_widgets_repository = self._init_widgets_repository(
            lst_custom_widgets=lst_custom_widgets
        )

        # We instantiate the config checker
        self._obj_config_checker = ConfigChecker(
            lst_widgets_json_schemas=[
                i_widget.get_dict_config_schema() for i_widget in self._dict_widgets_repository.values()
            ],
            str_base_json_schema_id="https://enovation.com/excel_dashboard"
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

    def _init_widgets_repository(
            self,
            lst_custom_widgets: list[Type[Widget]]
    ) -> dict[str, Type[Widget]]:
        """
        Function that builds the full list of widgets that can be later used by the ExcelDashboarder:
        - It dynamically screen the sub-directory "widgets", and search for the default widgets (aka the ones from
          com.enovation)
        - And it appends the custom widgets, if any.

        These widgets are not checked, so we might later end up discovering they are not properly configured/
        implemented (eg. no json schema file...).

        Two steps to discover and load the default widgets:
        - For a given directory path, we recursively load all python modules (aka files.py)
          https://stackoverflow.com/questions/3365740/how-to-import-all-submodules
        - Once all pythons modules are loaded, we can get all the widgets, as python classes deriving from Widget
          https://stackoverflow.com/questions/3862310/how-to-find-all-the-subclasses-of-a-class-given-its-name

        :param lst_custom_widgets: the custom widgets, to add on top of the default com.enovation ones
        :return: a list of class that extend class Widget
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        # We recursively import python modules under the sub-directory "widgets"
        # This is implemented in __init__.py, under the same package as this class

        # We initialize the repository of default widgets
        _dict_the_repository_of_widgets_classes: dict[str, Type[Widget]] = self._initialize_default_widgets_repository(
            cls_super_class=Widget
        )

        self._logger.debug(
            f"The ExcelDashboard application recognized '{len(_dict_the_repository_of_widgets_classes)}' widgets: "
            f"{', '.join(_dict_the_repository_of_widgets_classes)}"
        )

        # Eventually, we append the custom widgets provided: nothing to be done, as python classes for the widgets were
        # previously loaded, so they were found from the above _initialize_default_widgets_repository.
        # We will just check they are effectively available in the list
        _missing_widgets: list[str] = [
            i_widget.get_widget_id() for i_widget in lst_custom_widgets
            if i_widget.get_widget_id() not in _dict_the_repository_of_widgets_classes
        ]
        if len(_missing_widgets) > 0:
            self._logger.error(f"Some custom widgets could not be registered... they will be discarded: "
                               f"{', '.join(_missing_widgets)}")

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning a dictionary "
                           f"containing '{len(_dict_the_repository_of_widgets_classes)}' records.")
        return _dict_the_repository_of_widgets_classes

    def _initialize_default_widgets_repository(
            self,
            cls_super_class: Type[Widget]
    ) -> dict[str, Type[Widget]]:
        """
        Function that registers all widgets, aka python classes that extend the "Widget" class, directly or indirectly.
        Illustration: class A extends class B that extends class C that ... extends class Z that extends "Widget"
        - Classes A to Y indirectly extend "Widget"
        - Class Z extend directly "Widget"
        - All classes A to Z will be returned
        :return: the full list of widget classes, as a dictionary: $id -> widget class
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        _dict_the_return: dict[str, Type[Widget]] = {
            i_class.get_widget_id(): i_class for i_class in cls_super_class.__subclasses__()
        }

        for i_sub_class in cls_super_class.__subclasses__():
            _dict_the_return |= self._initialize_default_widgets_repository(cls_super_class=i_sub_class)

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")
        return _dict_the_return

    def excelize(
            self,
            p_output_file_path: Path,
            dict_config: dict,
            **dict_raw_parameters
    ):
        """
        :param p_output_file_path:
        :param dict_config:
        :param dict_raw_parameters: the named parameters that are required by the widgets being used
        :return:
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        # We check the excel configuration
        self._obj_config_checker.validate(dict_config)

        # We initialize the default formats
        self._initialize_default_formats(dict_config=dict_config)

        # We go through the configuration, consuming the parameters, and instantiating the widgets
        dict_the_widgets: dict[str, Widget] = self._instantiate_widgets(
            dict_repository_of_widgets=self._dict_widgets_repository,
            dict_config=dict_config,
            dict_raw_parameters=dict_raw_parameters
        )

        # We produce the excel spreadsheet
        self._produce_excel(
            p_output_file_path=p_output_file_path,
            dict_widgets=dict_the_widgets,
            dict_config=dict_config
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

    def _initialize_default_formats(
            self,
            dict_config: dict,
    ):
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        Widget.set_dict_wb_default_format(dict_config.get(self.const_str__config_label__str_format, {}))

        for k_sheet, v_sheet in dict_config[self.const_str__config_label__str_sheets].items():
            Widget.add_dict_ws_default_format(
                str_sheet_name=k_sheet,
                dict_default_format=v_sheet.get(self.const_str__config_label__str_format, {})
            )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

    def _instantiate_widgets(
            self,
            dict_repository_of_widgets: dict,
            dict_config: dict,
            dict_raw_parameters: dict
    ) -> dict[str, Widget]:
        """
        Function that check the parameter dict_config provided as an input:
        - If parameter is correct, the function is returning (no value returned)
        - Otherwise, an exception is thrown.

        The logic checks widget by widget the deeper structure of the json config.

        :param dict_repository_of_widgets: the repository of the widgets
        :param dict_config: the widget configuration
        :param dict_raw_parameters: the parameters provided to the module
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        dict_the_return: dict[str, Widget] = {}

        # We loop through each sheet
        for i_sheet_name, i_sheet in dict_config[self.const_str__config_label__str_sheets].items():

            # We loop through each widget
            for i_widget_label, i_widget in i_sheet[self.const_str__config_label__str_widgets].items():

                if i_widget_label in dict_the_return:
                    raise Exception(f"'{i_widget_label}' is defined several times in the configuration file, which is "
                                    f"not expected.")

                # We instantiate, and register, the widget
                # Note: while instantiating, parameters and configuration are checked...
                dict_the_return[i_widget_label] = dict_repository_of_widgets[
                    i_widget[Widget.const_str__config__widget_id]
                ](
                    str_address=i_widget[self.const_str__config_label__str_address],
                    dict_parameters_map=i_widget.get(self.const_str__config_label__str_parameters_map, {}),
                    dict_config=i_widget.get(self.const_str__config_label__str_config, {}),

                    # We only select the expected parameters, that we map to the labels expected by the widget
                    dict_raw_parameters=dict_raw_parameters,

                    str_sheet_name=i_sheet_name,
                    dict_default_format=i_widget.get(self.const_str__config_label__str_format, {})
                )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

        return dict_the_return

    def _produce_excel(
            self,
            p_output_file_path: Path,
            dict_widgets: dict,
            dict_config: dict,
    ) -> None:

        # We instantiate the Excel Writer, and get the workbook instance

        # We instantiate the excel
        xls_the_writer: ExcelWriter = ExcelWriter(
            path=p_output_file_path,
            engine='xlsxwriter'
        )
        wb_the_workbook: Workbook = xls_the_writer.book

        # We initialize the workbook properties
        self._initialize_workbook_properties(
            wb_the_workbook=wb_the_workbook,
            dict_config=dict_config,
        )

        # For each worksheet
        for k_sheet, v_sheet in dict_config[self.const_str__config_label__str_sheets].items():

            # We instantiate the worksheet
            ws_the_worksheet: Worksheet = self._instantiate_worksheet(
                str_worksheet_label=k_sheet,
                dict_worksheet_config=v_sheet,
                wb_workbook=wb_the_workbook
            )

            # We freeze panes
            if self.const_str__config_label__str_ws_freeze_panes in v_sheet:
                ws_the_worksheet.freeze_panes(**v_sheet[self.const_str__config_label__str_ws_freeze_panes])

            # We write the widgets
            for k_widget, v_widget in v_sheet[self.const_str__config_label__str_widgets].items():
                dict_widgets[k_widget].write_to_excel(
                    wb_workbook=wb_the_workbook,
                    ws_worksheet=ws_the_worksheet
                )

        # We handle VBAs, if any
        if self.const_str__config_label__str_vba in dict_config:

            _dict_vba_config: dict = dict_config[self.const_str__config_label__str_vba]

            # We check the VBA file
            if not isfile(_dict_vba_config[self.const_str__config_label__str_add_vba_project]):
                raise Exception(
                    f"The vba source file '{_dict_vba_config[self.const_str__config_label__str_add_vba_project]}' does "
                    f"not exist, which is not expected."
                )

            # If the VBA file is correct, we associate it to the workbook
            wb_the_workbook.add_vba_project(_dict_vba_config[self.const_str__config_label__str_add_vba_project])

            # We check if we have some VBA name to set
            if self.const_str__config_label__str_wb_set_vba_name in _dict_vba_config:
                wb_the_workbook.set_vba_name(_dict_vba_config[self.const_str__config_label__str_wb_set_vba_name])
            for k_ws, v_ws in _dict_vba_config.get(self.const_str__config_label__str_ws_set_vba_name, {}).items():
                _ws: Worksheet = wb_the_workbook.get_worksheet_by_name(k_ws)
                if _ws is None:
                    raise Exception(f"Worksheet '{k_ws}' does not exist, which is not expected.")
                _ws.set_vba_name(v_ws)

        # # Previously, we had to do the below trick, as 2 files were persisted:
        # # - One proper xlsm file
        # # - One buggy xlsx file, that we had to remove...
        # # Eventually, end of Dec 2022, this issue is not faced anymore... So we can get rid of the below trick.
        #     # Close the Pandas Excel writer and output the Excel file.
        #     xls_the_writer.close()
        #
        #     # Bug two files are generated, the expected xlsm and a buggy xlsx that needs to be removed...
        #     _path_xlsx_file: Path = p_output_file_path.with_suffix('.xlsx')
        #     if _path_xlsx_file.is_file():
        #         self._logger.debug(f"We are deleting the xlsx file generated by default...")
        #         os.remove(_path_xlsx_file)
        #     else:
        #         raise Exception(f"We are expecting a buggy xlsx file to be deleted, at path '{_path_xlsx_file}'... "
        #                         f"We could not find it, so we did not delete it!")
        #
        # # No VBA. We simply close the file...
        # else:

        # Close the Pandas Excel writer and output the Excel file.
        xls_the_writer.close()

    def _initialize_workbook_properties(
            self,
            wb_the_workbook: Workbook,
            dict_config: dict,
    ) -> Workbook:
        """
        Instantiate
        :param dict_config:
        :return:
        """

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        # We set properties
        if self.const_str__config_label__str_wb_set_properties in dict_config:
            dt_the_created_date = dict_config["workbook.set_properties"].get("created", datetime.now())
            if isinstance(dt_the_created_date, str):
                dt_the_created_date = datetime.fromisoformat(dt_the_created_date)
            wb_the_workbook.set_properties({
                'title': dict_config["workbook.set_properties"].get("title", "com.enovation - default title"),
                'subject': dict_config["workbook.set_properties"].get("subject", "com.enovation - default subject"),
                'author': dict_config["workbook.set_properties"].get("author", "com.enovation - default author"),
                'manager': dict_config["workbook.set_properties"].get("manager", "com.enovation - default manager"),
                'company': dict_config["workbook.set_properties"].get("company", "com.enovation - default company"),
                'category': dict_config["workbook.set_properties"].get("category", "com.enovation - default category"),
                'keywords': dict_config["workbook.set_properties"].get("keywords", "com.enovation default keywords"),
                'created': dt_the_created_date,
                'comments': dict_config["workbook.set_properties"].get("comments", "com.enovation - default comments"),
            })
        else:
            wb_the_workbook.set_properties({
                'title': "com.enovation - default title",
                'subject': "com.enovation - default subject",
                'author': "com.enovation - default author",
                'manager': "com.enovation - default manager",
                'company': "com.enovation - default company",
                'category': "com.enovation - default category",
                'keywords': "com.enovation default keywords",
                'created': datetime.now(),
                'comments': "com.enovation - default comments",
            })

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

        return wb_the_workbook

    def _instantiate_worksheet(
            self,
            str_worksheet_label: str,
            dict_worksheet_config: dict,
            wb_workbook: Workbook
    ) -> Worksheet:

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        # We instantiate the worksheet
        ws_the_worksheet: Worksheet = wb_workbook.add_worksheet(name=str_worksheet_label)
        ws_the_worksheet.hide_gridlines(option=2)

        # for each "worksheet.set_column"
        if self.const_str__config_label__str_ws_set_column in dict_worksheet_config:
            for i_set_column in dict_worksheet_config[self.const_str__config_label__str_ws_set_column]:

                # We instantiate the cell format, if any was provided
                dict_the_format: dict = i_set_column.get("cell_format", None)
                obj_the_format: Optional[Format] = None
                if dict_the_format is not None:
                    obj_the_format = wb_workbook.add_format(dict_the_format)

                # We set the column(s)...
                ws_the_worksheet.set_column(
                    first_col=i_set_column["first_col"],
                    last_col=i_set_column["last_col"],
                    width=i_set_column.get("width", None),
                    cell_format=obj_the_format,
                    options=i_set_column.get("options", None),
                )

        # We check if the sheet is to be hidden
        if dict_worksheet_config.get(self.const_str__config_label__str_worksheet_hide, False):
            ws_the_worksheet.hide()

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

        return ws_the_worksheet
