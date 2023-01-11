from typing import Any, Callable

import solara


@solara.component
def DataTable(df, on_drop_column: Callable[[str], Any] = None, on_filter_value: Callable[[str, int], Any] = None):
    def on_local_on_drop_column(column):
        if on_drop_column:
            on_drop_column(column)

    def on_local_filter_value(column, row_index):
        if on_filter_value:
            on_filter_value(column, row_index)

    column_actions = [solara.ColumnAction(icon="mdi-table-column-remove", name="drop column", on_click=on_local_on_drop_column)]
    cell_actions = [solara.CellAction(icon="mdi-filter", name="Filter values like this", on_click=on_local_filter_value)]
    return solara.DataTable(df, column_actions=column_actions, cell_actions=cell_actions, items_per_page=10, scrollable=True)
