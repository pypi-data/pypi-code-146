from collections import defaultdict
from functools import partial
import re
from typing import Callable, Dict, List, Tuple
import uuid

from IPython.display import display
from IPython.display import HTML
from ipywidgets import Layout
from ipywidgets import widgets
import numpy as np
import pandas as pd
from traitlets import Int
from traitlets import link
from traitlets import List as ListTrait
from traitlets import Unicode


@widgets.register
class RecordIDSelector(widgets.HBox, widgets.ValueWidget):
    value = Int().tag(sync=True)
    records = ListTrait().tag(sync=True)
    description = Unicode().tag(sync=True)


@widgets.register
class RecordTokenIDSelector(widgets.Dropdown, widgets.ValueWidget):
    token_idx = Int().tag(sync=True)
    ngram_row_idx = Int(-1).tag(sync=True)
    ngram_token_idxs = ListTrait([]).tag(sync=True)


@widgets.register
class ConfusionMatrixSelector(widgets.HBox, widgets.ValueWidget):
    value = ListTrait().tag(sync=True)
    group_name = Unicode().tag(sync=True)
    description = Unicode().tag(sync=True)


@widgets.register
class InteractiveDataFrame(widgets.VBox, widgets.ValueWidget):
    # NOTE: Using strings for typing selected row, col
    # Seems to be a ipywidgets bug where changing val to 0 can't be observed
    selected_row = Unicode().tag(sync=True)
    selected_col = Unicode().tag(sync=True)
    selected_area = Unicode().tag(sync=True)
    description = Unicode().tag(sync=True)


def disable_output_scroll():
    script = """
        <style>
       .jupyter-widgets-output-area .output_scroll {
            height: unset !important;
            border-radius: unset !important;
            -webkit-box-shadow: unset !important;
            box-shadow: unset !important;
        }
        .jupyter-widgets-output-area  {
            height: auto !important;
        }
    </style>
    """
    display(HTML(script))


def get_interactive_df(
    df: pd.DataFrame,
    *,
    display_cols: List[str] = None,
    bold_row: int = None,
    row_change_callback: Callable = None,
    col_change_callback: Callable = None
):
    disable_output_scroll()
    table_widget = None

    def on_change(change):
        cls = change['new'].split(' ')
        row = col = ""
        area = ""
        if len(cls) == 2:
            table_widget.selected_area = cls[0]
            col = re.search(r'\d+', cls[1]).group(0)
        elif len(cls) == 3:
            table_widget.selected_area = cls[0]
            if 'row' in cls[1]:
                row = re.search(r'\d+', cls[1]).group(0)
            if 'col' in cls[2]:
                col = re.search(r'\d+', cls[2]).group(0)
        table_widget.selected_area = area
        table_widget.selected_row = row
        table_widget.selected_col = col

    def style_table(styler):
        styler.set_uuid(table_key)
        if bold_row not in set([None, -1]):
            subset = pd.IndexSlice[display_df.index[display_df.index ==
                                                    bold_row], :]
            styler.applymap(lambda x: "font-weight: bold", subset=subset)
        styler.hide_index()
        return styler

    # Define table ID for selectors
    table_key = f"_interactive_df_table_{uuid.uuid4().hex}"
    status_key = f'{table_key}_selected_cell'

    # Injecting some JS to add clickhandlers for row, col in DF widget.
    script = """
    <script>
    var input
    var xpath = "//input[contains(@placeholder,'%s')]";

    function addHandlers() {
        input = document.evaluate(xpath, document, null, 
            XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        input.setAttribute("hidden","");

        var table = document.querySelector("#T_%s");
        var headcells = [].slice.call(table.getElementsByTagName("th"));
        var datacells = [].slice.call(table.getElementsByTagName("td"));
        var cells = headcells.concat(datacells);
        for (var i=0; i < cells.length; i++) {
        var createClickHandler = function(cell) {
            return function() { 
                input = document.evaluate(xpath, document, null,
                    XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                input.value = cell.className; 
                var event = new Event('change', { bubbles: true });
                input.dispatchEvent(event);
        }}
        cells[i].onclick = createClickHandler(cells[i]);
        };
    }
    window.onload = setTimeout(addHandlers, 500);
    </script>
    """ % (status_key, table_key)
    # add click handlers to cells
    display(HTML(script))

    # Create selected cell widget
    selected_cell = widgets.Text(placeholder=status_key)
    selected_cell.observe(on_change, 'value')

    display_df = df[display_cols] if display_cols else df

    table = widgets.Output()
    with table:
        # add table to output
        display(display_df.style.pipe(style_table))

    def row_cb_trans(change):
        val = change['new']
        if val.isdigit():
            val = int(val)
            return row_change_callback(df.iloc[val])

    def col_cb_trans(change):
        val = change['new']
        if val.isdigit():
            val = int(val)
            return col_change_callback(display_df[display_df.columns[val]])

    table_widget = InteractiveDataFrame([table, selected_cell])

    if row_change_callback:
        table_widget.observe(row_cb_trans, 'selected_row')
    if col_change_callback:
        table_widget.observe(col_cb_trans, 'selected_col')
    return table_widget


def tab_container(tab_names: List[str], tab_contents: List):
    tab_container = widgets.Tab()
    tab_container.children = tab_contents
    for i, name in enumerate(tab_names):
        tab_container.set_title(i, name)
    return tab_container


def record_id_nav(
    records: List[Tuple[int, int]], add_na=True
) -> RecordIDSelector:
    """

    Args:
        records (List[Tuple): Should be in form [(original_idx, data_idx)]
        original_idx is the record ID set by the user and used for display purposes
        data_idx is the index of the record in TruEra artifact storage.

    Returns:
        RecordIDSelector: the widget for record ID selection. widget.value is the data_idx of the selected record
    """

    # idx = 0
    inc_value = widgets.Button(description="+", layout=Layout(width='40px'))
    dec_value = widgets.Button(description="-", layout=Layout(width='40px'))
    dec_value.disabled = True

    dropdown = widgets.Dropdown(
        options=records,
        value=records[0][1],
        description=f"Record IDs ({len(records)}):",
        style={'description_width': 'initial'}
    )
    selector = RecordIDSelector(
        [dropdown, inc_value, dec_value], records=records
    )

    def inc_dec(_, inc):
        idx = dropdown.index
        if idx is None:
            return
        idx = idx + 1 if inc else idx - 1
        max_idx = len(dropdown.options) - 1
        idx = max(min(idx, max_idx), 0)
        dropdown.value = dropdown.options[idx][1]

    def handle_records_change(_):
        idx = dropdown.index
        if len(dropdown.options) > 0:
            dropdown.value = dropdown.options[idx][1]
        else:
            dropdown.value = -1
        dropdown.description = f"Record IDs ({len(dropdown.options)}):"

    def plus_minus_interactivity(change):
        new_idx = change['new']
        if new_idx is None:
            inc_value.disabled = dec_value.disabled = True
        max_idx = len(dropdown.options) - 1
        inc_value.disabled = new_idx == max_idx
        dec_value.disabled = new_idx == 0

    # Link dropdown and selector values and options
    link(
        (selector, 'value'), (dropdown, 'value')
    )  # allows user input via dropdown
    link(
        (selector, 'records'), (dropdown, 'options')
    )  # allows update dropdown options when selector records change

    # controls +/- enabled/disabled
    dropdown.observe(plus_minus_interactivity, 'index')
    # enables +/- functionality
    inc_value.on_click(partial(inc_dec, inc=True))
    dec_value.on_click(partial(inc_dec, inc=False))

    # What happens when records list changes
    selector.observe(handle_records_change, 'records')
    return selector


def confusion_matrix_nav(group_ind_dict: Dict[str, List[int]]):

    def handle_show_all_click(_):
        if binary_classification:
            cm_cls.value = "All"
        else:
            cm_gt_cls.value = "All"
            cm_pred_cls.value = "All"

    def handle_cls_change(_):
        if binary_classification:
            cm_widget.value = gt_pred_tree[cm_cls.value]
            cm_widget.group_name = cm_cls.value
        else:
            cm_widget.value = gt_pred_tree[cm_gt_cls.value][cm_pred_cls.value]
            cm_widget.group_name = f"(label={cm_gt_cls.value}, pred={cm_pred_cls.value})"

    classes = []
    gt_pred_tree = defaultdict(dict)

    binary_classification = False
    for key, idxs in group_ind_dict.items():
        if key == "All":
            continue  # add All later
        if "_as_" in key:
            gt, pred = key.split("_as_")
            classes.extend([gt, pred])
            gt_pred_tree[gt][pred] = list(idxs)

            if pred not in gt_pred_tree["All"]:
                gt_pred_tree["All"][pred] = set(idxs)
            else:
                gt_pred_tree["All"][pred] |= set(idxs)
        else:
            binary_classification = True
            classes.append(key)
            gt_pred_tree[key] = list(idxs)

    if binary_classification:
        gt_pred_tree["All"] = sorted(list(group_ind_dict['All']))
    else:
        # All: set to sorted list
        gt_pred_tree["All"] = {
            pred: sorted(list(v)) for pred, v in gt_pred_tree["All"].items()
        }
        # Get sorted list All for each gt key
        for v in gt_pred_tree.values():
            all_set = set()
            for sub_v in v.values():
                all_set |= set(sub_v)
            v['All'] = sorted(list(all_set))

    classes = ['All'] + sorted(list(set(classes)))

    cm_label = widgets.Label("Confusion Matrix Cell:")
    cm_show_all = widgets.Button(
        description="Show All", layout=Layout(width='auto')
    )

    cm_show_all.on_click(handle_show_all_click)
    if binary_classification:
        cm_cls = widgets.Dropdown(
            options=classes, value="All", layout=Layout(width='auto')
        )
        cm_cls.observe(handle_cls_change)
        elems = [cm_label, cm_cls, cm_show_all]
    else:

        cm_gt_cls = widgets.Dropdown(
            options=classes, value=classes[0], layout=Layout(width='auto')
        )
        cm_as = widgets.Label(
            "predicted as", layout=Layout(margin="2px 5px 2px 5px")
        )
        cm_pred_cls = widgets.Dropdown(
            options=classes, value=classes[0], layout=Layout(width='auto')
        )

        cm_gt_cls.observe(handle_cls_change)
        cm_pred_cls.observe(handle_cls_change)
        elems = [cm_label, cm_gt_cls, cm_as, cm_pred_cls, cm_show_all]

    cm_widget = ConfusionMatrixSelector(elems)
    if binary_classification:
        cm_widget.value = gt_pred_tree['All']
    else:
        cm_widget.value = gt_pred_tree['All']['All']
    return cm_widget


def ngram_correlation_table_widget(
    corrs: np.ndarray,
    corr_idx_mapping: List[int],
    tokens: List[str],
    token_influences: pd.DataFrame,
    *,
    selected_ngram_row_idx: int = None,
    max_ngram_size: int = 3,
    var_threshold: float = .025,
    ngram_limit: int = 20,
    row_change_callback: Callable = None,
    col_change_callback: Callable = None
):
    assert max_ngram_size >= 2
    corr_idx_mapping = np.array(corr_idx_mapping)
    corr_tokens = np.array([tokens[i] for i in corr_idx_mapping])

    vars = np.var(corrs, axis=1)
    var_threshold_filter = vars > var_threshold
    while var_threshold_filter.sum() < 5:
        var_threshold *= .8
        var_threshold_filter = vars > var_threshold

    # Filter out tokens with low correlation variance
    corr_sorted = corrs.argsort(axis=1)

    source_tokens = []
    ngram_token_idxs = []
    ngram_tokens = []
    ngram_infls = []
    ngram_agg_corrs = []

    for ngram_size in range(2, max_ngram_size + 1):
        ngrams = corr_sorted[:, -ngram_size:][:, ::-1]
        ngram_corrs = np.take_along_axis(corrs, ngrams, axis=1)

        # Filter out tokens with low correlation variance
        ngrams = ngrams[var_threshold_filter]
        ngram_corrs = ngram_corrs[var_threshold_filter]

        # Filter out duplicates
        ngrams, unique_idxs = np.unique(
            np.sort(ngrams, axis=1), return_index=True, axis=0
        )
        ngram_corrs = ngram_corrs[unique_idxs]

        # add to list
        source_tokens.append(corr_idx_mapping[ngrams[:, 0]].tolist())
        ngram_token_idxs.extend(corr_idx_mapping[ngrams].tolist())
        ngram_tokens.append(
            [" ".join(ngram) for ngram in corr_tokens[ngrams].tolist()]
        )
        ngram_infls.append(token_influences[ngrams].sum(axis=1))
        ngram_agg_corrs.append(ngram_corrs[:, 1:].mean(axis=1))

    source_tokens = np.concatenate(source_tokens)
    ngram_tokens = np.concatenate(ngram_tokens)
    ngram_infls = np.concatenate(ngram_infls)
    ngram_agg_corrs = np.concatenate(ngram_agg_corrs)

    ngram_df = pd.DataFrame(
        {
            "tokens": ngram_tokens,
            "ngram_influence": ngram_infls,
            "ngram_correlation": ngram_agg_corrs,
            "source_token_idx": source_tokens,
            "token_idxs": ngram_token_idxs,
        }
    )
    ngram_df = ngram_df.sort_values('ngram_correlation',
                                    ascending=False).reset_index()
    ngram_df = ngram_df.head(ngram_limit)
    return get_interactive_df(
        ngram_df,
        display_cols=['tokens', 'ngram_influence', 'ngram_correlation'],
        bold_row=selected_ngram_row_idx,
        row_change_callback=row_change_callback,
        col_change_callback=col_change_callback
    )
