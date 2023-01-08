from inspect import stack
from logging import Logger, getLogger

from dash import callback, Output, Input
from dash.html import P

import com.enovation.toolbox.predictability.dp_date_predictability.dp_grapher.dp_grapher_wid as wid
from com.enovation.toolbox.predictability.dp_date_predictability.dp_grapher.dp_grapher_session import Session

_logger: Logger = getLogger(__name__)


@callback(
    Output(wid.str_the_wid__debug_as_samp, 'children'),
    Input(wid.str_the_wid__debug_as_interval, 'n_intervals'),
)
def _callback_debug(i_interval_n: int) -> list[P]:
    """
    Callback function to update the debug
    :param i_interval_n: number of seconds since the application started
    :return:
    """
    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called with parameter i_interval_n = "
                  f"{i_interval_n}, and returning.")

    return Session.get_debug()
