from inspect import stack
from logging import Logger, getLogger
from typing import Union


class Session:
    """
    The class session is used to persist on the server side data related to the user's session.

    Among other things, the class is used to keep track for:
    - The debug trace: whenever we want to debug an information, we can call the function "debug", which will append
      the message and display the whole trace into the web browser (if debug option is activated)
    """

    _logger: Logger = getLogger(__name__)

    # ################################################################################################################ #
    # The logged message, to be printed in the debug                                                                   #
    # ################################################################################################################ #

    @property
    def lst_str_debug_trace(self) -> list[str]:
        return self._lst_str_debug_trace

    @property
    def dash_application(self) -> object:
        return self._dash_application

    @property
    def dict_sheets(self) -> dict:
        return self._dash_application.dict_sheets

    @property
    def dict_context(self) -> dict:
        return self._dash_application.dict_context

    @property
    def dict_config(self) -> dict:
        return self._dash_application.dict_config

    def __init__(
            self,
            dash_application
    ):
        # The dictionary is organized by session id, and then provide the list of all debut messages
        self._lst_str_debug_trace: list[str] = []
        self._dash_application = dash_application

    def debug(self, debug_trace: Union[str, list[str]]):
        """
        Function that logs new messages to be printed.

        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called with parameters:"
                           f"\n\tdebug_trace type : '{type(debug_trace)}'"
                           f"\n\tdebug_trace value: '{debug_trace}'.")

        lst_the_list_of_traces: list[str]

        if isinstance(debug_trace, str):
            self.lst_str_debug_trace.append(debug_trace)
        else:
            self._lst_str_debug_trace = self.lst_str_debug_trace

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
