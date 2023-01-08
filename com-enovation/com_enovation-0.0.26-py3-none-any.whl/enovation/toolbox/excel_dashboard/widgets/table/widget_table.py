from inspect import stack
from logging import Logger, getLogger
from typing import Optional

from pandas import DataFrame
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from com.enovation.toolbox.excel_dashboard.widgets.widget import Widget


class WidgetTable(Widget):
    """
    Widget that prints a table in the Excel Spreadsheet.

    Configuration:
    - The options when calling the function worksheet.add_table. See website for further details
      https://xlsxwriter.readthedocs.io/working_with_tables.html

    Parameters:
    - "df_data": the data, as a dataframe, to print into the table.
    """

    # The labels to parse the json configuration file
    const_str__config_label__str_columns: str = "columns"
    const_str__config_label__str_options: str = "options"
    const_str__config_label__str_conditional_formattings: str = "conditional_formattings"
    const_str__config_label__str_formula: str = "formula"
    const_str__config_label__str_multi_range: str = "multi_range"
    const_str__config_label__str_header_format: str = "header_format"
    const_str__config_label__str_format: str = "format"
    const_str__config_label__str_header: str = "header"
    const_str__config_label__str_range: str = "range"
    const_str__config_label__str_criteria: str = "criteria"
    const_str__config_label__str_type: str = "type"

    # The labels for the parameters expected by the widget
    const_str__parameter_label__df_data: DataFrame = "df_data"

    _logger: Logger = getLogger(__name__)

    @property
    def dict_options(self) -> dict:
        return self._dict_options

    @property
    def df_data(self) -> DataFrame:
        return self._df_data

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
        self._dict_options: Optional[dict] = None
        self._df_data: Optional[DataFrame] = None

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

        Properties for widget_table are:
        - dict_options
        - df_data

        :param dict_parameters: the parameters provided to the module
        :param dict_config: the configuration of the module
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        # We check the configuration
        self._dict_options = dict_config[self.const_str__config_label__str_options]

        # We check the parameters
        try:
            self._df_data = dict_parameters[
                self.const_str__parameter_label__df_data
            ]
        except KeyError:
            raise Exception(f"Parameter '{self.const_str__parameter_label__df_data}' could not be found, which "
                            f"is not expected.")

        # We check we have the proper number of columns:
        # - The columns in the dataframe on one side
        # - The "non-formula" columns configured in the table on the other side.
        _lst_non_formula_columns: list = [
            i_col[self.const_str__config_label__str_header]
            for i_col in self.dict_options[self.const_str__config_label__str_columns]
            if self.const_str__config_label__str_formula not in i_col
        ]
        if len(self.df_data.columns) != len(_lst_non_formula_columns):
            raise Exception(f"We do not have a coherent number of columns, as [A] should equal [C]:"
                            f"\n\t- [A] df_data contains '{len(self.df_data.columns)}' records"
                            f"\n\t- [B] configuration contains in total '"
                            f"{len(self.dict_options[self.const_str__config_label__str_columns])}' columns"
                            f"\n\t- [C] among which, '{len(_lst_non_formula_columns)}' are non formula.")

        # Addendum as of 02-Jan-2023: not unit tested!
        # We check columns have unique label...
        _lst_all_columns: list = [
            i_col[self.const_str__config_label__str_header]
            for i_col in self.dict_options[self.const_str__config_label__str_columns]
        ]
        if len(_lst_all_columns) != len(set(_lst_all_columns)):
            # We have duplicated columns! that is not expected...
            for i_col in set(_lst_all_columns):
                _lst_all_columns.remove(i_col)
            raise Exception(
                f"In the configuration of the widget Table, you mentioned several columns with the same labels... "
                f"Check columns labelled '{', '.join(_lst_all_columns)}'."
            )

        # We set the conditional formattings
        self.set_conditional_formattings(
            lst_conditional_formattings=dict_config.get(
                self.const_str__config_label__str_conditional_formattings, []
            ),
            str_reference_address=self.str_address,
            str_row_range_limit="2:"+str(len(self.df_data.index))
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

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

        # For each and every "formula" columns:
        # - 1. We add an empty columns in the df_data dataframe that will be printed
        #      This is required, or the whole dataframe is printed, and formula columns in between 2 columns would
        #      be overridden, and not appear
        # - 2 and 3. We instantiate the "format objects" from the "config properties"
        _data = self.df_data.copy()
        _index: int = 0
        if self.const_str__config_label__str_columns in self.dict_options:
            for i_column in self.dict_options[self.const_str__config_label__str_columns]:

                # 1. is there a formula defined?
                if self.const_str__config_label__str_formula in i_column:
                    # noinspection PyTypeChecker
                    _data.insert(_index, column="jsg", value=None, allow_duplicates=True)

                _index += 1

                # 2. is there "header_format" defined?
                if self.const_str__config_label__str_header_format in i_column:
                    i_column[self.const_str__config_label__str_header_format] = self.get_format(
                        dict_format=i_column[self.const_str__config_label__str_header_format],
                        wb_workbook=wb_workbook
                    )

                # 3. is there "format" defined?
                if self.const_str__config_label__str_format in i_column:
                    i_column[self.const_str__config_label__str_format] = self.get_format(
                        dict_format=i_column[self.const_str__config_label__str_format],
                        wb_workbook=wb_workbook
                    )
                else:
                    i_column[self.const_str__config_label__str_format] = self.get_format(
                        dict_format={},
                        wb_workbook=wb_workbook
                    )

        (_first_row, _first_col) = self.tpl_address
        _last_row = _first_row + len(self.df_data.index) + 1
        _last_col = _first_col + len(self.dict_options[self.const_str__config_label__str_columns]) - 1

        _options: dict = self._dict_options.copy()
        _options["data"] = _data.values.tolist()

        ws_worksheet.add_table(
            first_row=_first_row,
            first_col=_first_col,
            last_row=_last_row,
            last_col=_last_col,
            options=_options
        )

        # We eventually have to override all the formula columns... That is required in case "format" are defined, as
        # they somehow override the formulas...
        _i_col: int = _first_col
        if self.const_str__config_label__str_columns in self.dict_options:
            for i_column in self.dict_options[self.const_str__config_label__str_columns]:

                # is there a formula defined?
                if self.const_str__config_label__str_formula in i_column:

                    # We will print the same formula in each and every row
                    for _i_row in range(len(self.df_data.index)):
                        ws_worksheet.write_formula(
                            row=_first_row + _i_row + 1,
                            col=_i_col,
                            formula=i_column[self.const_str__config_label__str_formula],
                            cell_format=i_column.get(self.const_str__config_label__str_format, None),
                        )

                _i_col += 1

        # We eventually write the conditional formattings
        self.write_conditional_formattings(
            wb_workbook=wb_workbook,
            ws_worksheet=ws_worksheet
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
