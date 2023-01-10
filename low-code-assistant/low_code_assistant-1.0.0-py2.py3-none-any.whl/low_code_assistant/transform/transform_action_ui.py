from dataclasses import replace
from typing import Callable, Type, Union

import reacton
import reacton.ipyvuetify as v
import solara as sol

from low_code_assistant import action
from low_code_assistant.util import is_valid_variable_name


@reacton.component
def FilterPanel(columns, dtypes, on_action, fill):
    state, set_state = reacton.use_state(fill)

    def make_action():
        on_action(state)

    with sol.Div().meta(ref="FilterPanel") as panel:
        with sol.Div():
            FilterPanelView(columns, dtypes, state, set_state)

        with v.CardActions():
            v.Spacer()
            sol.Button(
                "apply",
                color="primary",
                icon_name="mdi-check",
                disabled=not state.is_valid(),
                on_click=make_action,
            )
    return panel


def escape_special_chars(s):
    return s.replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r") if s else s


def unescape_special_chars(s):
    return s.replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r") if s else s


@reacton.component
def FilterPanelView(columns, dtypes, action_: action.ActionFilter, on_filter_action):
    with sol.Div().meta(ref="FilterPanel") as main:
        with v.Row():
            with v.Col():
                v.Select(label="Column", v_model=action_.col, items=columns, on_v_model=lambda v: on_filter_action(replace(action_, col=v, dtype=dtypes[v])))
            with v.Col():
                v.Select(
                    label="Operator",
                    v_model=action_.op,
                    items=["<", ">", "<=", ">=", "!=", "=="],
                    on_v_model=lambda v: on_filter_action(replace(action_, op=v)),
                )
            with v.Col():

                def is_float_or_nan(value):
                    if value == "nan":
                        return True
                    try:
                        float(value)
                        return True
                    except ValueError:
                        return False

                v.TextField(
                    label="Value",
                    v_model=escape_special_chars(action_.value),
                    on_v_model=lambda v: on_filter_action(replace(action_, value=unescape_special_chars(v))),
                    error_messages=['Invalid value, consider using "as string"']
                    if action_.value and not action_.is_string and not is_float_or_nan(action_.value)
                    else None,
                )
            with v.Col():
                v.Switch(label="as string", v_model=action_.is_string, on_v_model=lambda v: on_filter_action(replace(action_, is_string=v)))
        with v.Row():
            with v.Col(sm=4):
                valid_variable_name = is_valid_variable_name(action_.df_var_out)
                v.TextField(
                    label="New dataframe name",
                    v_model=action_.df_var_out,
                    on_v_model=lambda v: on_filter_action(replace(action_, df_var_out=v)),
                    error_messages=[] if valid_variable_name else ["Invalid variable name"],
                )

    return main


@reacton.component
def SelectColumnsPanelView(columns, dtypes, action_: Union[action.ActionSelectColumns, action.ActionDropColumns], on_columns_action):
    with sol.Div().meta(ref="SelectColumnsPanel") as main:
        with v.Row():
            with v.Col():
                v.Select(
                    label="Columns",
                    v_model=action_.columns,
                    items=columns,
                    on_v_model=lambda v: on_columns_action(replace(action_, columns=v)),
                    multiple=True,
                    deletable_chips=True,
                )
        with v.Row():
            with v.Col():
                valid_variable_name = is_valid_variable_name(action_.df_var_out)
                v.TextField(
                    label="New dataframe name",
                    v_model=action_.df_var_out,
                    on_v_model=lambda v: on_columns_action(replace(action_, df_var_out=v)),
                    error_messages=[] if valid_variable_name else ["Invalid variable name"],
                )
    return main


@reacton.component
def GroupByPanelView(columns, dtypes, action_: action.ActionGroupBy, on_group_by_action):
    with sol.Div().meta(ref="GroupByPanel") as main:
        with v.Row():
            with v.Col(sm=4):
                v.Select(
                    label="Columns to group by",
                    v_model=action_.columns,
                    items=columns,
                    on_v_model=lambda v: on_group_by_action(replace(action_, columns=v)),
                    multiple=True,
                    deletable_chips=True,
                )
            with v.Col(sm=8, class_="pa-0"):
                new_aggs = []
                i = 0
                agg_names = ["size", "sum", "mean", "min", "max"]
                # filter out empty entries
                aggs = action_.aggregations and [k for k in action_.aggregations if not all(el is None for el in k)]
                for col, agg in aggs or []:
                    with v.Row():
                        with v.Col():
                            colnew = sol.ui_dropdown("Column to aggregate", col, columns, key=f"col_{i}")
                        with v.Col():
                            aggnew = sol.ui_dropdown("Aggregator", agg, agg_names, key=f"agg_{i}")
                            new_aggs.append((colnew, aggnew))
                            i += -1

                with v.Row():
                    with v.Col():
                        col = sol.ui_dropdown("Column to aggregate", None, columns, key=f"col_{i}")
                    with v.Col():
                        agg_name = sol.ui_dropdown("Aggregator", None, agg_names, key=f"agg_{i}")
                        if col and agg_name:
                            new_aggs.append((col, agg_name))

                on_group_by_action(replace(action_, aggregations=new_aggs))
        with v.Row():
            with v.Col(sm=4):
                valid_variable_name = is_valid_variable_name(action_.df_var_out)
                v.TextField(
                    label="New dataframe name",
                    v_model=action_.df_var_out,
                    on_v_model=lambda v: on_group_by_action(replace(action_, df_var_out=v)),
                    error_messages=[] if valid_variable_name else ["Invalid variable name"],
                )

    return main


@reacton.component
def TransformActionSelectPanel(
    columns,
    dtypes,
    action_: action.Action,
    on_action,
    on_action_type: Callable[[Type[Union[action.ActionFilter, action.ActionSelectColumns, action.ActionDropColumns, action.ActionGroupBy]]], None],
):
    action_mapping = {
        action.ActionFilter: "Filter rows",
        action.ActionDropColumns: "Drop columns",
        action.ActionSelectColumns: "Select columns",
        action.ActionGroupBy: "Groupby and aggregate",
    }
    action_mapping_reverse = {val: k for k, val in action_mapping.items()}

    op = action_mapping[type(action_)]

    def get_panel():
        if isinstance(action_, action.ActionFilter):
            return FilterPanelView(columns, dtypes, action_, on_action).key("filter_rows")
        if isinstance(action_, action.ActionDropColumns):
            return SelectColumnsPanelView(columns, dtypes, action_, on_action).key("drop columns")
        if isinstance(action_, action.ActionSelectColumns):
            return SelectColumnsPanelView(columns, dtypes, action_, on_action).key("select columns")
        if isinstance(action_, action.ActionGroupBy):
            return GroupByPanelView(columns, dtypes, action_, on_action).key("group by")

    with v.Sheet() as main:
        v.Select(
            label="Transformation",
            v_model=op,
            items=list(action_mapping.values()),
            on_v_model=lambda v: on_action_type(action_mapping_reverse[v]),  # type: ignore
        )
        if op is not None:
            get_panel()

    return main
