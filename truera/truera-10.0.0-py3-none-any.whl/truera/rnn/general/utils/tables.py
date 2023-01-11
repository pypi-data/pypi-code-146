from dash import dash_table
from dash import html
from dash.dash_table.Format import Format
from dash.dash_table.Format import Scheme
import dash_bootstrap_components as dbc
import pandas as pd
from pandas.api.types import is_numeric_dtype


def get_dash_table_from_df(df, table_id):
    column_dtypes = df.dtypes

    column_names = list(df.columns)
    mapper = lambda x: 'table-{}-col'.format(x)
    df = df.rename(mapper, axis='columns')
    column_ids = list(df.columns)
    column_dtypes = [is_numeric_dtype(df[c]) for c in df.columns]
    table_columns = [
        _get_dash_table_column_format(col_id, col_name, is_numeric=col_dtype)
        for col_id, col_name, col_dtype in
        zip(column_ids, column_names, column_dtypes)
    ]
    table = dash_table.DataTable(
        id=table_id,
        columns=table_columns,
        data=df.to_dict('records'),
        style_cell={'textAlign': 'center'},
        style_as_list_view=True,
    ),
    return table


def _get_dash_table_column_format(
    col_id, col_name, is_numeric=False, float_precision=4
):
    default_format = {'id': col_id, 'name': col_name}
    if is_numeric:
        default_format['type'] = 'numeric'
        default_format['format'] = Format(
            scheme=Scheme.fixed,
            precision=float_precision,
        )

    return default_format


def get_html_table_headers(col_names, align_center=False):
    style = {'text-align': 'center'} if align_center else {}
    return html.Thead(
        html.Tr([html.Th(c) for c in col_names]),
        className="truera-thead",
        style=style
    )


def get_html_table_rows(rows, align_center=False):
    style = {'text-align': 'center'} if align_center else {}
    return html.Tbody(
        [html.Tr([html.Td(col) for col in row]) for row in rows],
        className="truera-tbody",
        style=style
    )


def get_html_table(col_names, rows, align_center=False):
    return dbc.Table(
        [
            get_html_table_headers(col_names, align_center=align_center),
            get_html_table_rows(rows, align_center=align_center)
        ]
    )


def get_chunked_table(iterable, n=2):

    def chunk_iterable(lst, n):
        for i in range(0, len(lst), n):
            chunk = lst[i:i + n]
            chunk += ['' for _ in range(n - len(chunk))]
            yield chunk

    iterable_chunked = list(chunk_iterable(iterable, n))
    return dbc.Table(
        get_html_table_rows(iterable_chunked),
        bordered=True,
        style={'border-spacing': '10px'}
    )
