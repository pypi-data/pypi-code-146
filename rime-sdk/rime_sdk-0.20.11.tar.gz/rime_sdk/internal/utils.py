"""General Utilities."""


from html import escape
from typing import Dict, Optional, Sequence

HEADER_TMPL = "<th>{0}</th>"
DATA_TMPL = "<td>{0}</td>"
ROW_TMPL = "<tr>{0}</tr>"
TABLE_TMPL = '<table style="width:100%">{0}</table>'


def make_link(link: str, link_text: Optional[str] = None) -> str:
    """Make the HTML link."""
    if not link_text:
        link_text = "Link"
    return f'<a href="{link}" target="_blank" rel="noopener">{escape(link_text)}</a>'


def get_header_row_string(column_headers: Sequence[str]) -> str:
    """Return the table header row as a sring."""
    headers = [HEADER_TMPL.format(header) for header in column_headers]
    return ROW_TMPL.format("".join(headers))


def get_data_row_string(data_values: Sequence[str]) -> str:
    """Return a table data row as a string."""
    data = [DATA_TMPL.format(datum) for datum in data_values]
    return ROW_TMPL.format("".join(data))


def convert_dict_to_html(table_dict: Dict[str, str]) -> str:
    """Convert a dictionary to an HTML table."""
    if len(table_dict) == 0:
        return ""

    all_rows = [
        get_header_row_string(list(table_dict)),
        get_data_row_string(list(table_dict.values())),
    ]
    return TABLE_TMPL.format("".join(all_rows))
