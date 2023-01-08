from inspect import stack
from logging import Logger, getLogger
from typing import Optional

from xlsxwriter.utility import xl_cell_to_rowcol
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from com.enovation.toolbox.excel_dashboard.widgets.widget import Widget


class WidgetCoverSheet(Widget):
    """
    Simple widget that print a cover sheet in the Excel Spreadsheet.

    Configuration:
    - "narrative": the main text to print in the cover sheet. Texts to infer is handled through {}.
                   Illustration: 'Height: {0:f} {1:s}'.format(172.3, 'cm')

    Parameters:
    - "lst_tokens": list of tokens to infer into the narrative.
    """

    # The labels to parse the json configuration file
    const_str__config_label__str_narrative: str = "narrative"

    # The labels for the parameters expected by the widget
    const_str__parameter_label__lst_tokens: list = "tokens"

    _logger: Logger = getLogger(__name__)

    @property
    def str_narrative(self) -> str:
        return self._str_narrative

    @property
    def lst_tokens(self) -> list:
        return self._lst_tokens

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
        self._str_narrative: Optional[str] = None
        self._lst_tokens: Optional[list] = None

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

        # We check the configuration
        try:
            self._str_narrative = dict_config[
                self.const_str__config_label__str_narrative
            ]
        except KeyError:
            raise Exception(f"Configuration '{self.const_str__config_label__str_narrative}' could not be found, which "
                            f"is not expected.")

        # We check the parameters
        try:
            self._lst_tokens = dict_parameters[
                self.const_str__parameter_label__lst_tokens
            ]
        except KeyError:
            raise Exception(f"Parameter '{self.const_str__parameter_label__lst_tokens}' could not be found, which "
                            f"is not expected.")

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

        ws_worksheet.write(
            xl_cell_to_rowcol(self.str_address)[0],
            xl_cell_to_rowcol(self.str_address)[1],
            self.str_narrative.format(*self.lst_tokens)
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
