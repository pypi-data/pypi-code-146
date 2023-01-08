from inspect import stack
from logging import Logger, getLogger
from typing import Optional, Union

from xlsxwriter.format import Format
from xlsxwriter.utility import xl_cell_to_rowcol, xl_rowcol_to_cell
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from com.enovation.toolbox.excel_dashboard.cell_notation_helper import CellNotationHelper
from com.enovation.toolbox.excel_dashboard.widgets.widget import Widget


class WidgetTableZoom(Widget):
    """
    Widget that prints detailed characteristics for a given key from a table.

    Configuration:
    - The cell with the key to select the record to zoom from the table which contains all the details
    - The list of characteristics to display the one after the other, along with the following details:
      - The formula to get and display the values
      - The format
      - The conditional formatting.

    Parameters:
    - No parameter is provided.
    """

    # The labels to parse the json configuration file
    const_str__config_label__str_parameter: str = "parameter"
    const_str__config_label__str_value: str = "value"
    const_str__config_label__str_format: str = "format"
    const_str__config_label__str_conditional_formattings: str = "conditional_formattings"
    const_str__config_label__str_merged: str = "merged"

    const_str__function_label__str_merge_range: str = "merge_range"
    const_str__function_label__str_write: str = "write"
    const_str__function_label__str_function: str = "function"
    const_str__function_label__str_parameter: str = "parameter"

    # The labels for the parameters expected by the widget
    # Illustration: const_str__parameter_label__df_data: DataFrame = "df_data"

    _logger: Logger = getLogger(__name__)

    @property
    def dict_cells_or_ranges_to_write(self) -> dict:
        return self._dict_cells_or_ranges_to_write

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
        - Calling the Widget super init function
        - Declare the widget properties:
          - Each has their "property" getters
          - They are declared and instantiated to None
          - They are effectively set through the function "check_parameters_and_set_properties"

        :param str_address: the address in a sheet to print the widget
        :param dict_config: the widget configuration (aka the "config" node in the json)
        :param dict_parameters_map: the dictionary to map users parameters to the ones expected by the widget:
                                    - key: the expected label
                                    - value: the actual label
        :param dict_raw_parameters: the parameters as labelled and provided by the users
        :param str_sheet_name: the name of the sheet in which the widget is instantiated (required to handle default
            formats inheritance, from the workbook to the workshoeet to the widget)
        :param dict_default_format: the default format set at the level of the widget. If such default format is not
            configured, we expect an empty dictionary
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        # We declare the widget properties, initialized to None
        # Illustration: self._dict_options: Optional[dict] = None
        self._dict_cells_or_ranges_to_write: Optional[dict] = None
        # self._dict_options: Optional[dict] = None

        # The super init function initializes the widget:
        # - Step 1, we set the widget properties (from nodes from the json configuration): address, parameters map,
        #   config
        # - Step 2, we process the parameters:
        #   - Rename parameters to fit the labels as expected by the widget
        #   - Check parameters to ensure their values are correct, and set widget properties, to use these parameters
        #     while printing into the Excel spreadsheet --> function 'check_parameters_and_set_properties' to be
        #     overridden by each widget will call both the functions to check parameters and config
        super().__init__(
            str_address=str_address,
            dict_parameters_map=dict_parameters_map,
            dict_config=dict_config,
            dict_raw_parameters=dict_raw_parameters,
            str_sheet_name=str_sheet_name,
            dict_default_format=dict_default_format
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
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        # #####################################################@
        # We check the parameters

        # We screen the config, and append in a list the parameters to print
        _dict_the_parameters = self._get_parameters(
            config=dict_config,
            dict_parameters=dict_parameters
        )

        # We get the default format/ value/ parameter
        _dict_the_default_format: dict = dict_config.get(self.const_str__config_label__str_format, {})
        _str_the_default_parameter: str = dict_config.get(self.const_str__config_label__str_parameter, None)

        if _str_the_default_parameter is not None:
            _str_the_default_value: str = dict_parameters[_str_the_default_parameter]
        else:
            _str_the_default_value: str = dict_config.get(self.const_str__config_label__str_value, "")

        # We then process each area one by one

        self._dict_cells_or_ranges_to_write = {}

        for k, v in dict_config.items():
            # We ignore the keys "format", "value", "parameter" and "conditional formatting"
            if k in [
                self.const_str__config_label__str_format,
                self.const_str__config_label__str_value,
                self.const_str__config_label__str_parameter,
                self.const_str__config_label__str_conditional_formattings
            ]:
                pass

            else:
                self._dict_cells_or_ranges_to_write.update(
                    self._process_range(
                        str_reference_address=self.str_address,
                        dict_parameters=_dict_the_parameters,
                        str_address=k,
                        config=v,
                        dict_default_format=_dict_the_default_format,
                        default_value=_str_the_default_value
                    )
                )

        # We set the conditional formattings
        self.set_conditional_formattings(
            lst_conditional_formattings=dict_config.get(
                self.const_str__config_label__str_conditional_formattings, []
            ),
            str_reference_address=self.str_address,
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

    @staticmethod
    def _process_range(
            str_reference_address: str,
            str_address: str,
            config: Union[dict, list],
            dict_parameters: dict,
            dict_default_format: dict,
            default_value
    ) -> dict:
        """

        :param str_reference_address:
        :param str_address:
        :param config:
        :param dict_parameters:
        :param dict_default_format: cannot be None, only {}
        :param default_value: cannot be None, only ""
        :return:
        """
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        # These are the variables we will set, to eventually return a processed range
        _lst_the_cells_addresses: Optional[list[str]] = None
        _lst_the_formats: Optional[list[dict]] = None
        _lst_the_values: Optional[list] = None
        _lst_the_functions: Optional[list[str]] = None

        # We translate the address
        _str_translated_address: str = CellNotationHelper.translate_address_to_reference(
            str_reference_cell=str_reference_address,
            str_address=str_address
        )

        # We decompose the address into a list of cells:
        # - If address is a range, we get a list with all the cells contained in the range
        # - If address is one cell, we get a list with only this cell
        _lst_the_cells_addresses = WidgetTableZoom._for_each_cell_in_range(_str_translated_address)

        # If the configuration is of type "dictionary"
        if isinstance(config, dict):

            # ##########################################################################################################
            # We set the format
            _the_format_to_return: Union[dict, list] = config.get(
                WidgetTableZoom.const_str__config_label__str_format,
                dict_default_format
            )
            if isinstance(_the_format_to_return, list):
                _lst_the_formats = _the_format_to_return
            elif config.get(WidgetTableZoom.const_str__config_label__str_merged, False):
                _lst_the_formats = [_the_format_to_return]
            else:
                _lst_the_formats = [_the_format_to_return] * len(_lst_the_cells_addresses)

            # ##########################################################################################################
            # We set the value

            # Most simple case: we have straight value(s)
            if WidgetTableZoom.const_str__config_label__str_value in config:
                _the_value_to_return = config[WidgetTableZoom.const_str__config_label__str_value]

            # Else, if we have parameter(s) that we need to transcode:
            # - Either a list of parameters to transcode one by one
            # - Or one single parameter
            elif WidgetTableZoom.const_str__config_label__str_parameter in config:

                _the_value_to_return = config[WidgetTableZoom.const_str__config_label__str_parameter]

                if isinstance(_the_value_to_return, list):
                    _the_new_values_to_return: list = []
                    for i_value in _the_value_to_return:
                        if i_value not in dict_parameters:
                            raise Exception(f"Parameter '{i_value}' is missing.")
                        _the_new_values_to_return.append(dict_parameters[i_value])

                    _the_value_to_return = _the_new_values_to_return

                else:
                    if _the_value_to_return not in dict_parameters:
                        raise Exception(f"Parameter '{_the_value_to_return}' is missing.")
                    _the_value_to_return = dict_parameters[_the_value_to_return]

            # Else, we default the values
            else:
                _the_value_to_return = default_value

            # We now ensure the value is a list of values
            if isinstance(_the_value_to_return, list):
                _lst_the_values = _the_value_to_return
            elif config.get(WidgetTableZoom.const_str__config_label__str_merged, False):
                _lst_the_values = [_the_value_to_return]
            else:
                _lst_the_values = [_the_value_to_return] * len(_lst_the_cells_addresses)

            # We set the function
            if config.get(WidgetTableZoom.const_str__config_label__str_merged, False):
                _lst_the_functions = [WidgetTableZoom.const_str__function_label__str_merge_range]
            else:
                _lst_the_functions = [WidgetTableZoom.const_str__function_label__str_write] *\
                                     len(_lst_the_cells_addresses)

        # Else, the configuration is of type list
        else:

            _lst_the_formats = []
            _lst_the_values = []
            _lst_the_functions = []

            for i_config in config:

                # We set the format
                _dict_the_format_to_return: dict = i_config.get(
                    WidgetTableZoom.const_str__config_label__str_format,
                    dict_default_format
                )
                _lst_the_formats.append(_dict_the_format_to_return)

                # We set the value
                _the_value_to_return = i_config.get(
                    WidgetTableZoom.const_str__config_label__str_parameter,
                    i_config.get(
                        WidgetTableZoom.const_str__config_label__str_value,
                        default_value
                    )
                )
                _lst_the_values.append(_the_value_to_return)

                # We set the function
                _lst_the_functions.append(WidgetTableZoom.const_str__function_label__str_write)

        _int_the_range_size: int = len(_lst_the_cells_addresses)

        # If the area is to be merged
        if _lst_the_functions[0] == WidgetTableZoom.const_str__function_label__str_merge_range:

            # We check we have the proper number of records
            if (len(_lst_the_functions) != 1) \
                    | (len(_lst_the_formats) != 1) \
                    | (len(_lst_the_values) != 1):
                raise Exception(f"For the range '{str_address}' to merge, we have '{_int_the_range_size}' "
                                f"cells to process, but '{len(_lst_the_functions)}' functions, '{len(_lst_the_values)}'"
                                f" values and '{len(_lst_the_formats)}' formats. WE EXPECTED ALL TO BE ONE!")

            # Eventually, we produce the processed range
            _dict_the_return: dict = {
                _str_translated_address.replace("$", ""): {
                    # Function: "merge" or "write"
                    WidgetTableZoom.const_str__function_label__str_function: _lst_the_functions[0],

                    # Value and format
                    WidgetTableZoom.const_str__function_label__str_parameter: {
                        WidgetTableZoom.const_str__config_label__str_format: _lst_the_formats[0],
                        WidgetTableZoom.const_str__config_label__str_value: _lst_the_values[0]
                    }
                }
            }

        # Else, the area is not to be merged
        else:

            # We check we have the proper number of records
            if (len(_lst_the_functions) != _int_the_range_size) \
                    | (len(_lst_the_formats) != _int_the_range_size) \
                    | (len(_lst_the_values) != _int_the_range_size):
                raise Exception(f"For the range '{str_address}', we have '{_int_the_range_size}' cells to process, but "
                                f"'{len(_lst_the_functions)}' functions, '{len(_lst_the_values)}' values and "
                                f"'{len(_lst_the_formats)}' formats. WE EXPECTED ALL TO BE EQUAL TO "
                                f"'{_int_the_range_size}'")

            # Eventually, we produce the processed range
            _dict_the_return: dict = {}
            for i_cell in range(0, len(_lst_the_cells_addresses)):
                _dict_the_return[_lst_the_cells_addresses[i_cell]] = {
                    # Function: "merge" or "write"
                    WidgetTableZoom.const_str__function_label__str_function: _lst_the_functions[i_cell],

                    # Value and format
                    WidgetTableZoom.const_str__function_label__str_parameter: {
                        WidgetTableZoom.const_str__config_label__str_format: _lst_the_formats[i_cell],
                        WidgetTableZoom.const_str__config_label__str_value: _lst_the_values[i_cell]
                    }
                }

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return _dict_the_return

    @staticmethod
    def _for_each_cell_in_range(str_range: str) -> list[str]:
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        _lst_cells: list[str] = str_range.split(":")

        if len(_lst_cells) == 1:
            _lst_the_return: list[str] = [str_range.replace("$", "")]

        else:

            (_int_first_row, _int_first_col) = xl_cell_to_rowcol(_lst_cells[0])
            (_int_last_row, _int_last_col) = xl_cell_to_rowcol(_lst_cells[1])

            _lst_the_cell_as_row_col: list = [
                (i_row, i_col)
                for i_row in range(_int_first_row, _int_last_row+1) for i_col in range(_int_first_col, _int_last_col+1)
            ]

            _lst_the_return: list[str] = [
                xl_rowcol_to_cell(row=i_row_col[0], col=i_row_col[1])
                for i_row_col in _lst_the_cell_as_row_col
            ]

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return _lst_the_return

    @staticmethod
    def _get_parameters(
            config: Union[dict, list],
            dict_parameters: dict = None
    ) -> dict:
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        # We list the expected parameters
        _lst_the_parameters: list = WidgetTableZoom._list_parameters(config=config)

        # We check these expected parameters effectively exist
        _lst_the_diff: list = list(set(_lst_the_parameters) - set(dict_parameters.keys()))
        if len(_lst_the_diff) > 0:
            raise Exception(f"Configuration expects parameters which are not provided: {', '.join(_lst_the_diff)}")

        _dict_the_return: dict = {
            k: dict_parameters[k] for k in _lst_the_parameters
        }

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return _dict_the_return

    @staticmethod
    def _list_parameters(config: Union[dict, list]) -> list:
        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        _lst_the_return: list = []

        # If we screen a dictionary
        if isinstance(config, dict):

            # We screen each and every (key, value)
            for k, v in config.items():

                # If key is "parameter"
                if k == WidgetTableZoom.const_str__config_label__str_parameter:

                    # If value is a list
                    if isinstance(v, list):
                        _lst_the_return.extend(v)

                    # If value is not a list
                    else:
                        _lst_the_return.append(v)

                # Else, key is not "parameter
                # And if value is itself a dictionary or a list
                elif isinstance(v, (dict, list)):
                    _lst_the_return.extend(WidgetTableZoom._list_parameters(config=v))

        # Else, we screen a list
        else:

            # For each record in the list
            for v in config:

                # if value is itself a dictionary or a list
                if isinstance(v, (dict, list)):
                    _lst_the_return.extend(WidgetTableZoom._list_parameters(config=v))

        # We then remove duplicates
        _lst_the_return = list(dict.fromkeys(_lst_the_return))

        getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return _lst_the_return

    def write_to_excel(
            self,
            wb_workbook: Workbook,
            ws_worksheet: Worksheet,
    ):
        """
        Function that writes the widget into the excel spreadsheet. When called, the widget is fully initialized,
        with all its properties set.

        Note: it is while writing into excel that we transcode formats, from "format config" as dictionary to "format"
        object as expected by xlsxwriter.

        :param ws_worksheet: the worksheet to print the widget
        :param wb_workbook:
        """

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        for k, v in self.dict_cells_or_ranges_to_write.items():

            _str_the_function: str = v[self.const_str__function_label__str_function]

            _obj_the_format: Format = self.get_format(
                dict_format=v[self.const_str__config_label__str_parameter][self.const_str__config_label__str_format],
                wb_workbook=wb_workbook
            )

            if _str_the_function == self.const_str__function_label__str_write:
                ws_worksheet.write(
                    k,
                    v[self.const_str__config_label__str_parameter][self.const_str__config_label__str_value],
                    _obj_the_format
                )

            elif _str_the_function == self.const_str__function_label__str_merge_range:
                ws_worksheet.merge_range(
                    k,
                    v[self.const_str__config_label__str_parameter][self.const_str__config_label__str_value],
                    _obj_the_format
                )

            else:
                raise Exception(f"Function '{_str_the_function}' is unexpected.")

        # We eventually write the conditional formattings
        self.write_conditional_formattings(
            wb_workbook=wb_workbook,
            ws_worksheet=ws_worksheet
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
