from dash import html
import dash_bootstrap_components as dbc

import truera.rnn.general.utils.colors as Colors


def get_button_from_icon(button_id, icon_class, style={}):
    style.update({'color': Colors.TRUERA_GREEN})
    return dbc.Button(
        id=button_id,
        color='link',
        children=html.I(className=icon_class),
        style=style
    )
