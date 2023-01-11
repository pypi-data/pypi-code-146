import dash
import dash_bootstrap_components as dbc

import truera.rnn.general.utils.colors as Colors


def create_radio_items(id, options, default_value, inline=True):
    return dbc.RadioItems(
        id=id,
        options=options,
        value=default_value,
        inline=inline,
        className='truera-radioitems'
    )
