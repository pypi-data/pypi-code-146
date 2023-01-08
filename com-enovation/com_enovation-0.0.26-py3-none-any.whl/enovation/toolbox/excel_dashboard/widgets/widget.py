import collections.abc
import copy
import inspect
import json
from inspect import stack
from logging import Logger, getLogger
from pathlib import Path
from typing import Optional

from xlsxwriter.format import Format
from xlsxwriter.utility import xl_cell_to_rowcol
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from com.enovation.toolbox.excel_dashboard.cell_notation_helper import CellNotationHelper


def copy_then_update(d, u):
    return update(copy.deepcopy(d), u)


def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


class Widget:
    """
    Default class for widgets.

    A widget depends on 3 components:
    - Python code: logic to print the widget in an excel spreadsheet. eg. print a list of data which evolve over time
    - Json configuration: configuration of the widget for a given application. This configuration is used and reused as
      the application is run. eg. the columns to be printed in the list, along with their formattings
    - Parameters: particular context that is provided at each run of the application. eg. the data to print in the list

    To implement a widget, you have to go through the following steps:
    - Add a dedicated directory that will contain both:
      - The python code of the widget
      - The json schema file to validate widget configuration (same file name, replacing extension '.py' by '.json')
    - The python code of the widget should extend this Widget class
      - Override the function check_parameters: this function validates the parameters provided to the widget. eg. will
        check the configured columns to print in the list effectively exist in the dataframe containing the data to
        print (provided as a DataFrame parameter)
      - Override the function write_to_excel, which is where the logic to print the widget into excel lies.

    To support the above, each widget inherits from the following properties:
    - Class properties:
      - 'dict_config_schema': the json schema to check and validate the widget configuration. This is a class property
        as all instances of the same widget share the same json schema
    - Instance properties:
      - 'str_address': the address (in a sheet) to print the widget
      - 'dict_config': the configuration of the widget (validated against the schema 'dict_config_schema')
      - 'dict_parameters_map': the dictionary to map actual parameters names into the ones expected by the widget
      - 'dict_raw_parameters': the parameters as provided by the user to the widget (before being mapped into the
        parameters expected by the widget)

    TODO:
    - The default formats:
      - _dict_wb_default_format should be associated to the super class Widget, and not to sub_classes cls --> only one
        default across each an every Widget subclasses
      - _dict_ws_default_format should be associated to each and every Widget subclass, getting rid of the widget
        label...
    """

    const_str__class_attribute__dict_config_schema: str = "dict_config_schema"

    # Labels from json schema
    const_str__json_schema__widget_id: str = "$id"

    # Labels from configuration
    const_str__config__widget_id: str = "widget_id"

    # Labels from configuration for the conditional formattings
    const_str__config_label__str_options: str = "options"
    const_str__config_label__str_formula: str = "formula"
    const_str__config_label__str_multi_range: str = "multi_range"
    const_str__config_label__str_range: str = "range"
    const_str__config_label__str_criteria: str = "criteria"
    const_str__config_label__str_type: str = "type"
    const_str__config_label__str_format: str = "format"

    # There is a mechanism to set default formats at various levels in the application:
    # - Level 1: the entire workbook can have a default format
    # - Level 2: each worksheet can have their own default formats
    # - Level 3: each widget can have themselves their own default formats
    # Whenever default formats exist at various levels, the mechanism has the logic to consolidate.
    #
    # Illustration:
    # - The workbook has a default format level 1: wrap, color black
    # - The sheet has a default format level 2: underline
    # - The widget has a default format level 3: italic, color green
    # - The function get_format is called for a format: no italic
    # - The resulting format returned is: wrap, color green, underline, no italic
    #
    # The following properties and functions support this logic:
    # - _dict_wb_default_format: class property that contains the unique default format that is set at the level of
    #   the workbook
    # - _dict_ws_default_formats_raw: class property that contains the various default formats by worksheet. The
    #   worksheet label is used as the key. This is the raw format as configured, not inheriting from the default
    #   format level 1 set at the workbook level. The getter method dict_ws_default_formats will return the sheet
    #   clean format, inheriting from the default format level 1 set at the workbook level
    # - _dict_default_format_raw: instance property that contains the widget default format. This is the raw format as
    #   configured, not inheriting from the default formats level 1 or 2 set at the workbook or worksheet levels. The
    #   getter method dict_default_format will return the widget clean format, inheriting from both the default format
    #   levels 1 and 2, set at the workbook and worksheet levels
    _dict_wb_default_format: Optional[dict] = None

    @classmethod
    def set_dict_wb_default_format(cls, dict_default_format: dict):
        cls._dict_wb_default_format = dict_default_format

    @classmethod
    def get_dict_wb_default_format(cls) -> dict:
        if cls._dict_wb_default_format is None:
            getLogger(__name__).error(
                f"The class property _dict_wb_default_format was not initialized, which is not expected. "
                f"Ensure you call function set_dict_wb_default_format."
            )
            cls._dict_wb_default_format = {}
            # raise Exception("The class property _dict_wb_default_format was not initialized, which is not expected. "
            #                 "Ensure you call function set_dict_wb_default_format.")
        return cls._dict_wb_default_format

    _dict_ws_default_formats: dict = {}

    @classmethod
    def add_dict_ws_default_format(cls, str_sheet_name: str, dict_default_format: dict):
        if str_sheet_name in cls._dict_ws_default_formats:
            raise Exception(f"The class property _dict_ws_default_formats already has a default format for the sheet "
                            f"named '{str_sheet_name}', which is not expected. "
                            f"Ensure you call function add_dict_ws_default_format only once.")
        _dict_the_format: dict = cls.get_dict_wb_default_format()
        _dict_the_format = copy_then_update(_dict_the_format, dict_default_format)
        cls._dict_ws_default_formats[str_sheet_name] = _dict_the_format

    @classmethod
    def get_dict_ws_default_format(cls, str_sheet_name: str) -> dict:
        if str_sheet_name not in cls._dict_ws_default_formats:
            getLogger(__name__).error(
                f"The class property _dict_ws_default_formats does not have default format for the sheet "
                f"named '{str_sheet_name}', which is not expected. "
                f"Ensure you call function add_dict_ws_default_format, even with an empty dictionary."
            )
            cls.add_dict_ws_default_format(str_sheet_name=str_sheet_name, dict_default_format={})
        return cls._dict_ws_default_formats[str_sheet_name]

    def _get_dict_default_format(self, dict_default_format: dict, str_sheet_name: str) -> dict:
        # if self._dict_wb_default_format is None:
        #     self._logger.error(
        #         f"The class property _dict_wb_default_format was not initialized, which is not expected. "
        #         f"Ensure you call function set_dict_wb_default_format."
        #     )
        #     self._dict_wb_default_format = {}
        # if str_sheet_name not in self._dict_ws_default_formats:
        #     self._logger.error(
        #         f"The class property _dict_ws_default_formats already has a default format for the sheet "
        #         f"named '{str_sheet_name}', which is not expected. "
        #         f"Ensure you call function add_dict_ws_default_format only once."
        #     )
        #     self.add_dict_ws_default_format(str_sheet_name=str_sheet_name, dict_default_format={})

        _dict_the_format = self.get_dict_ws_default_format(str_sheet_name=str_sheet_name)
        _dict_the_format = copy_then_update(_dict_the_format, dict_default_format)
        return _dict_the_format

    @classmethod
    def reinitialize_default_formats(cls):
        cls._dict_wb_default_format = None
        cls._dict_ws_default_formats = {}

    _logger: Logger = getLogger(__name__)

    # the address (in a sheet) to print the widget
    @property
    def str_address(self) -> str:
        return self._str_address

    # the address (in a sheet) to print the widget as a tuple(row, col)
    @property
    def tpl_address(self) -> tuple[int, int]:
        return xl_cell_to_rowcol(self.str_address)

    # the map from actual parameters to the ones expected by the widget (only expected when these are different)
    # - key=expected parameter name, as the widget code will refer to
    # - value=actual parameter name, as provided by the wider application.
    @property
    def dict_parameters_map(self) -> dict:
        return self._dict_parameters_map

    # the configuration of the widget (validated against the schema 'dict_config_schema')
    @property
    def dict_config(self) -> dict:
        return self._dict_config

    # the raw parameters provided by the user, before they are renamed and checked
    @property
    def dict_raw_parameters(self) -> dict:
        return self._dict_raw_parameters

    # the default widget format, inheriting from the sheet and the workbook default formats
    @property
    def dict_default_format(self) -> dict:
        return self._dict_default_format

    @property
    def lst_conditional_formattings(self) -> list:
        return self._lst_conditional_formattings

    def __init__(
            self,
            str_address: str,
            dict_parameters_map: dict,
            dict_config: dict,
            dict_raw_parameters: dict,
            str_sheet_name: str,
            dict_default_format: dict
    ):
        """
        Initialize the widget:
        - Step 1, we set the widget properties:
          - from nodes in the json configuration: address, parameters map, config
          - from parameters: raw parameters
        - Step 2, we process the parameters:
          - Rename parameters to fit the labels as expected by the widget
          - Check parameters to ensure their values are correct, and set widget properties, to use these parameters
            while printing into the Excel spreadsheet --> function 'check_parameters_and_set_properties' to be
            overridden by each widget

        :param str_address: the address in a sheet to print the widget
        :param dict_config: the widget configuration (aka the "config" node in the json)
        :param dict_parameters_map: the dictionary to map users parameters to the ones expected by the widget:
                                    - key: the expected label
                                    - value: the actual label
        :param dict_raw_parameters: the parameters as labelled and provided by the users
        :param str_sheet_name: the name of the sheet in which the widget is instantiated (required to handle default
            formats inheritance, from the workbook to the worksheet to the widget)
        :param dict_default_format: the default format set at the level of the widget. If such default format is not
            configured, we expect an empty dictionary
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        # Step 1, we set the widget properties: address, config, parameters map, raw parameters
        self._str_address = str_address
        self._dict_config = copy.deepcopy(dict_config)  # Required, as we might transform some format in the config
        self._dict_parameters_map = dict_parameters_map
        self._dict_raw_parameters = dict_raw_parameters

        # Conditional formattings will be set through the dedicated function set_conditional_formattings, which is
        # called through the function check parameters and set properties
        self._lst_conditional_formattings: list[dict] = []

        # Step 1b, we instantiate the default format for the widget, inheriting from default formats set at the level
        # of the workbook and the worksheets
        self._dict_default_format = self._get_dict_default_format(
            dict_default_format=dict_default_format,
            str_sheet_name=str_sheet_name
        )

        # Step 2, we rename, check and get the widget parameters
        self._rename_check_and_set_properties(
            dict_parameters_map=self._dict_parameters_map,
            dict_config=self._dict_config,
            dict_raw_parameters=self._dict_raw_parameters
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

    def _rename_check_and_set_properties(
            self,
            dict_parameters_map: dict,
            dict_config: dict,
            dict_raw_parameters: dict,
    ):
        """
        Function that processes the parameters:
        - Rename parameters to fit the labels as expected by the widget
        - Check parameters to ensure their values are correct, and set the widget properties to be used
          while printing into the Excel spreadsheet --> function 'check_parameters_and_get_parameters' to be
          overridden by each widget.

        While renaming parameters, if an actual parameter name to map is missing, then an exception is raised.

        :param dict_parameters_map: dictionary to map the actual parameters into the ones expected by the widget
                                    - key: expected parameter name, as referenced within the widget
                                    - value: actual parameter name, as provided as part of the wider application
        :param dict_config: dictionary with the widget configuration
        :param dict_raw_parameters: dictionary that contains the raw parameters to rename into the ones expected by the
                                    widget
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        # We initialize the dictionary to update the parameters
        dict_renamed_parameters: dict = {}

        # Step 1, we rename the parameters, using the parameters map
        for k_expected, v_actual in dict_parameters_map.items():
            if v_actual in dict_raw_parameters:
                dict_renamed_parameters[k_expected] = dict_raw_parameters[v_actual]

            else:
                raise Exception(f"When trying to map parameter '{k_expected}' expected by the widget, the actual "
                                f"parameter '{v_actual}' could not be found.")

        # We duplicate the dictionary with all parameters, that we update with renamed parameters
        dict_raw_and_renamed_parameters: dict = dict(dict_raw_parameters)
        dict_raw_and_renamed_parameters.update(dict_renamed_parameters)

        # We eventually call the function 'check_parameters_and_get_parameters' that is to be overridden by each widget
        self.check_parameters_and_set_properties(
            dict_parameters=dict_raw_and_renamed_parameters,
            dict_config=dict_config,
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

    def check_parameters_and_set_properties(
            self,
            dict_parameters: dict,
            dict_config: dict,
    ):
        """
        Function that checks the parameters that are required by the widget:
        - If all expected parameters are correct, the widget properties are set and the function returns (no value
          returned)
        - Otherwise, an exception is thrown.

        Checking parameters means:
        - Check the parameter exists, in case it is a mandatory one. eg. mandatory array of data to print in a list
        - Check the format is as expected. eg. has to be a DataFrame
        - Check the values are correct. eg. numeric vs alpha, etc.
        - Check coherence with config. eg. columns configured as "to be printed" effectively exist in the DataFrame.

        Setting properties means:
        - Set the widget instance properties from the parameters/ config
        - So these properties can later be used while writing into Excel.

        Properties for widget_cover_sheet are:
        - str_narrative
        - lst_tokens

        :param dict_parameters: the parameters provided to the module
        :param dict_config: the configuration of the module
        """
        raise Exception(f"Function to be overridden...")

    def get_format(
            self,
            dict_format: dict,
            wb_workbook: Workbook
    ) -> Format:
        """
        Function that define a format object, from its properties.

        :param dict_format:
        :param wb_workbook:
        :return:
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        _dict_the_format: dict = copy_then_update(
            self.dict_default_format,
            dict_format
        )

        _format: Format = wb_workbook.add_format(properties=_dict_the_format)

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return _format

    def set_conditional_formattings(
            self,
            lst_conditional_formattings: list[dict],
            str_reference_address: str,
            str_column_range_limit: str = None,
            str_row_range_limit: str = None
    ):
        """
        Function that processes the conditional formattings configured, and transform the following attributes:
        - The "range"
        - The "options"."multi_range", if it exists
        - The "options"."criteria" for the conditional formatting "options"."type"=="formula"

        This function is called from the sub-widget classes, when the function check_parameters_and_set_properties is
        called
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        for i_conditional_formatting in lst_conditional_formattings:

            _dict_i_conditional_formatting: dict = copy.deepcopy(i_conditional_formatting)

            # We process the range
            _dict_i_conditional_formatting[Widget.const_str__config_label__str_range] = \
                Widget._process_conditional_formatting__range(
                    str_range=i_conditional_formatting[Widget.const_str__config_label__str_range],
                    str_reference_address=str_reference_address,
                    str_column_range_limit=str_column_range_limit,
                    str_row_range_limit=str_row_range_limit
                )

            # We process the multi-range, if any
            if Widget.const_str__config_label__str_multi_range in \
                    _dict_i_conditional_formatting[Widget.const_str__config_label__str_options]:
                _dict_i_conditional_formatting[
                    Widget.const_str__config_label__str_options][
                    Widget.const_str__config_label__str_multi_range] = \
                    Widget._process_conditional_formatting__multi_range(
                        str_multi_range=i_conditional_formatting[
                            Widget.const_str__config_label__str_options][
                            Widget.const_str__config_label__str_multi_range],
                        str_reference_address=str_reference_address,
                    str_column_range_limit=str_column_range_limit,
                    str_row_range_limit=str_row_range_limit
                    )

            # If the conditional formatting contains a formula
            if _dict_i_conditional_formatting[
                Widget.const_str__config_label__str_options][
                Widget.const_str__config_label__str_type] == \
                    Widget.const_str__config_label__str_formula:
                _dict_i_conditional_formatting[
                    Widget.const_str__config_label__str_options][
                    Widget.const_str__config_label__str_criteria] = \
                    Widget._process_conditional_formatting__formula(
                        str_formula=i_conditional_formatting[
                            Widget.const_str__config_label__str_options][
                            Widget.const_str__config_label__str_criteria],
                        str_reference_address=str_reference_address
                    )

            self._lst_conditional_formattings.append(_dict_i_conditional_formatting)

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

    @staticmethod
    def _process_conditional_formatting__range(
            str_range: str,
            str_reference_address: str,
            str_column_range_limit: str = None,
            str_row_range_limit: str = None
    ) -> str:
        """
        Function that processes a range for a given conditional formatting. It receives a range or cell address, and
        seeks to:
        - Translate it relative to a reference address,
        - Transform it, if expressed as a column or a row, into a range.

        The limits are set relatively to the widget, and have to be translated to the reference cell

        An exception is thrown in case:
        - The input range is not pattern cell, range or column
        - The input range is a column or a row range, but there is not limit set (to transform into a full range)
        - There is any dollar in the range provided
        - The outputs range is not correct cell or range.

        A warning is logged in case there is any limit provided but not used.
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called with parameters:"
                                  f"\n\t- str_range: '{str_range}'"
                                  f"\n\t- str_reference_address: '{str_reference_address}'"
                                  f"\n\t- str_column_range_limit: '{str_column_range_limit}'"
                                  f"\n\t- str_row_range_limit: '{str_row_range_limit}'")

        _str_the_return: str = str_range

        # If we do not have a proper pattern for the input str_range, we raise an exception
        _str_the_pattern: str = CellNotationHelper.get_address_pattern(str_address=str_range)
        if (
                CellNotationHelper.is_pattern_cell(str_pattern=_str_the_pattern)
                | CellNotationHelper.is_pattern_range(str_pattern=_str_the_pattern)
                | CellNotationHelper.is_pattern_column(str_pattern=_str_the_pattern)
                | CellNotationHelper.is_pattern_row(str_pattern=_str_the_pattern)
        ) is False:
            raise Exception(f"The parameter str_range '{str_range}' has an incorrect pattern '{_str_the_pattern}'. "
                            f"It should be either a cell, a range or a column.")

        # If there is any dollar in the range provided
        if "$" in str_range:
            raise Exception(f"There is '$' in the parameter str_range='{str_range}', which is not expected.")

        # If we do receive column or row ranges, we need the associated limits
        if CellNotationHelper.is_pattern_column(str_pattern=_str_the_pattern):
            if str_row_range_limit is None:
                raise Exception(f"The parameter str_range '{str_range}' is a column range, but no str_row_range_limit "
                                f"is provided to transform it into a range... Which is not expected.")
            if str_column_range_limit:
                getLogger(__name__).warning(
                    f"The parameter str_range '{str_range}' is a column range, but one useless str_column_range_limit "
                    f"is provided... Only str_row_range_limit is required to transform it into a range... Maybe "
                    f"a configuration inconsistency?")

            # We override the column range with a range
            _str_the_return = CellNotationHelper.transform_columns_intersect_rows_into_range_or_cell(
                str_columns=_str_the_return,
                str_rows=CellNotationHelper.transform_address_into_relative_and_absolute_address(
                    str_address=str_row_range_limit,
                    b_first_row_at=True,
                    b_last_row_at=True
                ),
                b_check_correct=False
            )

        elif CellNotationHelper.is_pattern_row(str_pattern=_str_the_pattern):
            if str_column_range_limit is None:
                raise Exception(f"The parameter str_range '{str_range}' is a row range, but no str_column_range_limit "
                                f"is provided to transform it into a range... Which is not expected.")
            if str_row_range_limit:
                getLogger(__name__).warning(
                    f"The parameter str_range '{str_range}' is a row range, but one useless str_row_range_limit "
                    f"is provided... Only str_column_range_limit is required to transform it into a range... Maybe "
                    f"a configuration inconsistency?")

            # We override the row range with a range
            _str_the_return = CellNotationHelper.transform_columns_intersect_rows_into_range_or_cell(
                str_columns=CellNotationHelper.transform_address_into_relative_and_absolute_address(
                    str_address=str_column_range_limit,
                    b_first_col_at=True,
                    b_last_col_at=True
                ),
                str_rows=_str_the_return,
                b_check_correct=False
            )

        # We eventually translate the range vis-a-vis the reference
        _str_the_return = CellNotationHelper.translate_address_to_reference(
            str_address=_str_the_return,
            str_reference_cell=str_reference_address
        )

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning "
                                  f"'{_str_the_return}'.")
        return _str_the_return

    @staticmethod
    def _process_conditional_formatting__multi_range(
            str_multi_range: str,
            str_reference_address: str,
            str_column_range_limit: str = None,
            str_row_range_limit: str = None
    ) -> str:
        """
        Function that processes a multi-range for a given conditional formatting. Multi-range is configured as
        multiple range tokens that separated by space.

        The function will first tokenize the multi-range into range token, that can then be processed through the
        function _process_conditional_formatting__range.

        The function _process_conditional_formatting__range will:
        - Translate each range token relative to a reference address,
        - Transform each range token, if expressed as a column, into a range.

        Eventually, we concatenate the processed range tokens back into one single multi-range

        An exception is thrown in case:
        - The input multi-range has one range token:
          - Which is not pattern cell, range or column
          - Which is a column or a row range, but there is not limit set (to transform into a full range)
          - Which has any dollar
        - The outputs multi-range is not correct concatenation of cells or ranges.

        A warning is logged in case there is any limit provided but not used.
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called with parameters:"
                                  f"\n\t- str_multi_range: '{str_multi_range}'"
                                  f"\n\t- str_reference_address: '{str_reference_address}'"
                                  f"\n\t- str_column_range_limit: '{str_column_range_limit}'"
                                  f"\n\t- str_row_range_limit: '{str_row_range_limit}'")

        _lst_str_range_token: list[str] = str_multi_range.split()
        _lst_the_return: list[str] = []
        _str_the_return: str

        for i_range_token in _lst_str_range_token:
            _lst_the_return.append(
                Widget._process_conditional_formatting__range(
                    str_range=i_range_token,
                    str_reference_address=str_reference_address,
                    str_column_range_limit=str_column_range_limit,
                    str_row_range_limit=str_row_range_limit
                )
            )

        _str_the_return = " ".join(_lst_the_return)

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning "
                                  f"'{_str_the_return}'.")
        return _str_the_return

    @staticmethod
    def _process_conditional_formatting__formula(
            str_formula: str,
            str_reference_address: str
    ) -> str:
        """
        Function that processes a formula for a given conditional formatting. It receives a formula, and
        seeks to:
        - Translate the relative addresses to a reference, if any,
        - Transform them.

        Illustration: for reference address B3
        - @A would become: B
        - @A1 would become: B1
        - A@1 would become: A3
        - @A:@A would become: B:B
        - @1:@1 would become: 3:3

        An exception is thrown in case:
        - The formula cannot be processed
        - Any error in the addresses to transform.
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called with parameters:"
                                  f"\n\t- str_formula: '{str_formula}'"
                                  f"\n\t- str_reference_address: '{str_reference_address}'")

        _str_the_return: str = CellNotationHelper.translate_formula_to_reference(
            str_reference_address=str_reference_address,
            str_formula=str_formula
        )

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning "
                                  f"'{_str_the_return}'.")
        return _str_the_return

    def write_to_excel(
            self,
            wb_workbook: Workbook,
            ws_worksheet: Worksheet
    ):
        """
        Function that writes the widget into the excel spreadsheet. When called, the widget is fully initialized,
        with all its properties set.

        Note: it is while writing into excel that we
        - Transcode formats, from "format config" as dictionary to "format" object as expected by xlsxwriter, by
          calling the function get_format
        - Write the conditional formattings by calling the function the function write_conditional_formattings.

        :param ws_worksheet:
        :param wb_workbook:
        """
        raise Exception(f"Function to be overridden...")

    def write_conditional_formattings(
            self,
            wb_workbook: Workbook,
            ws_worksheet: Worksheet
    ):

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called .")

        # We add the conditional formattings
        for i_cond_format in self.lst_conditional_formattings:
            _str_the_range: str = i_cond_format[self.const_str__config_label__str_range]

            _dict_the_options: dict = i_cond_format[self.const_str__config_label__str_options]

            _dict_the_format: dict = _dict_the_options[self.const_str__config_label__str_format]

            _obj_the_format: Format = self.get_format(
                dict_format=_dict_the_format,
                wb_workbook=wb_workbook
            )

            _dict_the_options[self.const_str__config_label__str_format] = _obj_the_format

            ws_worksheet.conditional_format(
                _str_the_range,
                options=_dict_the_options
            )
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning .")

    @classmethod
    def get_dict_config_schema(
            cls,
    ) -> dict:
        """
        Function that returns the json schema to configure the widget. This json schema should comply to the following
        rules:
        - Should be labelled the same way as the python file
        - Except ".py" extension is "json".

        In case such a json does not exist, the function returns an empty dictionary.

        :return: the json schema as a dictionary to validate the configuration of the widget
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        # We get the class attribute "dict_config_schema"
        dict_the_return: dict = getattr(cls, Widget.const_str__class_attribute__dict_config_schema, None)

        # If the class attribute "dict_config_schema was not yet set
        if dict_the_return is None:

            # We get the file which defines the class
            _path_to_python_file: Path = Path(inspect.getfile(cls))
            _path_to_json_file: Path = _path_to_python_file.with_suffix('.json')
            if _path_to_json_file.is_file():
                try:
                    with _path_to_json_file.open() as _json_schema:
                        dict_the_return = json.load(_json_schema)
                except Exception as _exception:
                    raise Exception(f"Could not load json schema '{_json_schema}'.") from _exception
            else:
                raise Exception(f"When processing widget '{_path_to_python_file}', we could not find the "
                                f"associated json schema, expected under '{_path_to_json_file}'. This is not "
                                f"expected, and the process had to quit...")

            # We persist the class attribute for other instances of the widget
            setattr(cls, Widget.const_str__class_attribute__dict_config_schema, dict_the_return)

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

        return dict_the_return

    @classmethod
    def get_widget_id(
            cls,
    ) -> str:
        if cls.const_str__json_schema__widget_id not in cls.get_dict_config_schema():
            raise Exception(f"When processing widget '{cls}', could not find node "
                            f"'{cls.const_str__json_schema__widget_id}' in the json schema, which is not expected.")

        return cls.get_dict_config_schema()[cls.const_str__json_schema__widget_id]
