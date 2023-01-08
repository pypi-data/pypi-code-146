from inspect import stack
from logging import Logger, getLogger

from dash import callback, Output, Input, html

from com.enovation.toolbox.predictability.dp_date_predictability.dp_grapher.dp_grapher_session import Session
from com.enovation.toolbox.predictability.dp_date_predictability.dp_grapher.tab_p1_welcome.tab_welcome__as_div import \
    TabWelcomeAsDiv
import com.enovation.toolbox.predictability.dp_date_predictability.dp_grapher.dp_grapher_wid as wid
from com.enovation.toolbox.predictability.dp_date_predictability.dp_grapher.tab_p2_explore.tab_explore__as_div import \
    TabExploreAsDiv

_logger: Logger = getLogger(__name__)


@callback(
    Output(wid.str_the_wid__content_as_main, 'children'),
    Input(wid.str_the_wid__url_as_location, 'hash'),
    prevent_initial_call=True
)
def _callback_navigate_and_load_content(url_hash: str) -> html.Div:
    """
    Callback function to update the main content.
    :param url_hash:
    :return:
    """
    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

    if url_hash == '#explore':
        div_the_return: html.Div = TabExploreAsDiv()

    elif (url_hash == '#welcome') | (url_hash == ''):
        div_the_return: html.Div = TabWelcomeAsDiv()

    else:
        raise Exception(f"Unexpected url_hash '{url_hash}'.")

    if url_hash != '':
        Session.debug(debug_trace=f"Click navigation menus to update main content: {url_hash}")

    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

    return div_the_return
