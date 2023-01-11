import logging
import sys
from typing import Any, Callable, Dict, Tuple, Union

HAS_IPYTHON = True
try:
    from IPython.display import clear_output
    from IPython.display import display
except ImportError:
    HAS_IPYTHON = False

HAS_IPYWIDGETS = True
try:
    from ipywidgets import fixed
    from ipywidgets import HBox
    from ipywidgets import interact
    from ipywidgets import VBox
    from ipywidgets import widgets
except ImportError:
    HAS_IPYWIDGETS = False
import math

import numpy as np
from traitlets import dlink

from truera.client.nn.wrappers import nlp
from truera.nlp.general.aiq.components import confusion_matrix_nav
from truera.nlp.general.aiq.components import record_id_nav
from truera.nlp.general.aiq.components import RecordTokenIDSelector
from truera.nlp.general.aiq.filtering_utils import get_accuracy_group_name_dict
from truera.nlp.general.utils.configs import QoIType
from truera.nlp.general.utils.configs import TokenType
from truera.rnn.general.container import ArtifactsContainer

from .aiq import NlpAIQ
from .plots import NLPPlots

WIDGET_STYLE = dict(description_width='initial')


def interactive_output_override(
    f: Callable, controls: Dict[str, Union[widgets.Widget, Tuple[widgets.Widget,
                                                                 str]]]
) -> widgets.Output:
    """Overrides ipywidgets.interactive_output to handle passing in traits besides value. 
    This avoids the need for creating hidden widgets and instead allows using multiple traits from the same widget

    Args:
        f (Callable): Function to be called
        controls (Dict[str, Union[ipywidgets.Widget, Tuple[ipywidgets.Widget, str]]]): Each key, value can be one of two formats:
        {"arg_name": (widget, "widget_trait")}
            - Passes in widget.widget_trait as f(arg_name=widget.widget_trait)
        {"arg_name": widget}
            - Mirrors above behavior, but the widget_trait is defaulted to "value"

    Returns:
        ipywidgets.Output: Output display of f is captured and returned
    """
    out = widgets.Output()

    def observer(change):
        kwargs = {}
        for k, w in controls.items():
            value_name = "value"
            if isinstance(w, tuple):
                w, value_name = w
            kwargs[k] = getattr(w, value_name)
        widgets.interaction.show_inline_matplotlib_plots()
        with out:
            clear_output(wait=True)
            f(**kwargs)
            widgets.interaction.show_inline_matplotlib_plots()

    for w in controls.values():
        value_name = 'value'
        if isinstance(w, tuple):
            w, value_name = w
        w.observe(observer, value_name)
    widgets.interaction.show_inline_matplotlib_plots()
    observer(None)
    return out


def check_ipython(func):

    def wrapper(*args, **kwargs):
        if not HAS_IPYTHON:
            raise ImportError(
                "We require ipython. Consider installing via `pip install ipython`."
            )
        return func(*args, **kwargs)

    return wrapper


def check_ipywidgets(func):

    def wrapper(*args, **kwargs):
        if not HAS_IPYWIDGETS:
            raise ImportError(
                "We require ipywidgets. Consider installing via `pip install ipywidgets`."
            )
        return func(*args, **kwargs)

    return wrapper


def about(html):

    def decorator(func):

        def wrapper(*args, **kwargs):
            accordion = widgets.Accordion(
                children=[widgets.HTML(value=html,)], selected_index=None
            )
            accordion.set_title(0, 'About this Widget')
            display(accordion)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def nml(arr, sort=False):
    if sort:
        arrmax, arrmin = arr.min(), arr.max()
    else:
        arrmax, arrmin = arr.max(), arr.min()
    denom = arrmax - arrmin
    if denom == 0:
        denom += 10e-10  # fix invalid divide issues
    return (arr - arrmin) / denom


class Figures():

    def __init__(
        self,
        aiq: NlpAIQ,
        log_level: int = logging.INFO,
    ):
        self.aiq = aiq
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger(name="nlp-visualizations")

    def get_num_records(self, artifacts_container):
        num_records = self.aiq.model.get_default_num_records(
            artifacts_container
        )
        return num_records

    def get_token_widget(self):
        token_widget = widgets.Text(
            description='Token:',
            value='',
            placeholder='Type something',
            continuous_update=False,
            style=WIDGET_STYLE
        )
        return token_widget

    def get_exp_range_widget_options(
        self,
        *,
        min_val: int,
        max_val: int,
        num_nodes: int,
        first_tick: int,
        is_int: bool = True
    ) -> widgets.SelectionRangeSlider:
        """ Get a range widget that grows exponentially from min_val to max_val. 
        If integer slider, we want the min step to be 1, so if the exponential growth is less than 1, will increase by 1 instead.

        Args:
            min_val (int): minimum value of the widget.
            max_val (int): maximum value of the widget
            num_nodes (int): number of options in the widget.
            first_tick (int): The first tick of the range slider. 
            is_int (int): Whether this widget is for ints. if not, it will be floats.

        Returns:
            widgets.SelectionRangeSlider: The exponential slider widget
        """
        assert max_val >= min_val
        total_range = max_val - min_val
        if total_range == 0:
            return widgets.SelectionRangeSlider(
                options=[min_val], index=(0, 0), disabled=True
            )

        if is_int and num_nodes > total_range:
            # Cannot be more granular than 1 to 1, value to node. A step size is 1 or larger.
            num_nodes = total_range + 1
        if first_tick > num_nodes:
            first_tick = num_nodes - 1

        if is_int:
            exponent_base = total_range**(
                1 / (num_nodes - 1)
            )  # we want exponent_base^node_tick = value.
            options = [
                round(exponent_base**i) +
                min_val if round(exponent_base**i) > i else i + min_val
                for i in range(
                    1, num_nodes
                )  # if the exponential growth is less than linear, use linear instead.
            ]
        else:
            # We want base^node_tick = value + 1. This differs from integer widget because the exponential base is not the first tick.
            # The first tick for floats is exponential base - 1 (because exponential growth must have base greater than 1)
            exponent_base = (total_range + 1)**(1 / (num_nodes - 1))

            def to_sig_fig(exponent_base: float, i: int) -> float:
                """Helper method to convert floats to sig fig.

                Args:
                    exponent_base (float): the numeric base
                    i (int): the exponent

                Returns:
                    float: exponent_base**i, with sig figs of 3
                """
                x = exponent_base**i
                # This is mostly needed for string formatting on the slider, so just float-ify the desired string version
                return float(f"{x-1:.3}")

            options = [
                to_sig_fig(exponent_base, i) + min_val
                for i in range(1, num_nodes)
            ]
        options = [min_val] + options
        widget = widgets.SelectionRangeSlider(
            options=options, index=(first_tick, num_nodes - 1), disabled=False
        )
        return widget

    def get_influence_range_widget(
        self, artifacts_container: ArtifactsContainer, token_type: TokenType,
        num_records: int, offset: int
    ) -> widgets.SelectionRangeSlider:
        """_summary_

        Args:
            artifacts_container (ArtifactsContainer): The artifacts metadata
            token_type (TokenType): The type of token (token or word)
            num_records (int): The number of records to use.
            offset (int): The starting record to get.

        Returns:
            The range selector for influences.
        """
        _, influences, _, _, _, _, _, _ = self.aiq.model.get_artifacts_metadata(
            artifacts_container,
            token_type=token_type,
            num_records=num_records,
            offset=offset
        )
        return self.get_exp_range_widget_options(
            min_val=0,
            max_val=np.max(np.abs(influences)),
            num_nodes=40,
            first_tick=2,
            is_int=False
        )

    def get_influence_range_examples_widget(self):
        influence_range_examples_widget = widgets.FloatRangeSlider(
            value=[0, 0],
            min=0,
            max=0,
            description='Influence Range:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='.2f',
            style=WIDGET_STYLE
        )
        return influence_range_examples_widget

    def get_dropdown_widget(
        self, multi_class_segment_metrics, value, description
    ):
        dropdown_widget = widgets.Dropdown(
            options=list(multi_class_segment_metrics.keys()),
            value=value,
            description=description,
            disabled=False,
        )
        return dropdown_widget

    def get_class_widget(self, num_classes):
        class_widget = widgets.BoundedIntText(
            value=0,
            min=0,
            max=num_classes - 1,
            step=1,
            description='Class ID:',
            style=WIDGET_STYLE,
            disabled=False
        )
        return class_widget

    def get_infl_histogram_widget(
        self, token_widget, num_classes, error_driver_group_dict, empty_message
    ):
        infl_histogram = widgets.interactive_output(
            NLPPlots.token_influence_histogram,
            dict(
                highlight_token=token_widget,
                num_classes=fixed(num_classes),
                group=fixed('All'),
                error_driver_group_dict=fixed(error_driver_group_dict),
                empty_message=fixed(empty_message),
            )
        )
        return infl_histogram

    @check_ipython
    @check_ipywidgets
    @about(
        html=
        "Compare the influence distributions of a token from different segments to see if the model uses them differently. </br></br>The segment metrics widget can help find tokens that cause the model treats differently per segment."
    )
    def token_influence_comparison_segment(
        self,
        token_frequency,
        influences_dict,
        artifacts_container: ArtifactsContainer,
        max_words_to_track=500,
        offset=0,
        token_type=TokenType.WORD
    ):
        """
        Compute the histogram with token influences for a pair of segments.
        Args: 
            - Artifacts container
            - Max words to track - Default is 500. We usually track 30k tokens
            - offset - Default is 0
            - Token type - Default to TokenType.WORD
        Returns: An interactive widget with histogram of influence values and examples from the segments.
        """
        qoi_type = QoIType.CLASS_WISE
        NUM_SEGMENTS = 2
        multi_class_segment_metrics = self.aiq.segment_output_metrics_info(
            artifacts_container
        )
        num_classes = self.aiq.model.get_num_classes(artifacts_container)
        num_records = self.get_num_records(artifacts_container)
        error_driver_group_dict = self.aiq.global_explanations_error_driver_info(
            artifacts_container, num_records, max_words_to_track, offset,
            token_type
        )
        token_widget = self.get_token_widget()
        widgets.Dropdown.value.tag(sync=True)
        segment_1_widget = self.get_dropdown_widget(
            multi_class_segment_metrics, value='total', description='Segment 1'
        )
        segment_2_widget = self.get_dropdown_widget(
            multi_class_segment_metrics, value='total', description='Segment 2'
        )
        widgets.Dropdown.value.tag(sync=True)

        influence_range_examples_widget = self.get_influence_range_examples_widget(
        )

        infl_examples_options = [influence_range_examples_widget]

        class_widget = self.get_class_widget(num_classes)

        infl_examples_options.append(class_widget)

        influences_df = self.aiq.model.get_artifacts_df(
            artifacts_container,
            token_type=token_type,
            num_records=num_records,
            offset=offset
        )

        infl_examples_options = widgets.VBox(infl_examples_options)
        empty_message = 'No instances of that token in the current split.'

        def update_influence_range(
            min, max, influence_range_widget=influence_range_examples_widget
        ):
            influence_range_widget.min, influence_range_widget.max = min, max

        def update_influence_value(
            min,
            max,
            class_idx=0,
            class_widget=class_widget,
            influence_range_widget=influence_range_examples_widget
        ):
            influence_range_widget.value = [min, max]

        infl_hist = widgets.interactive_output(
            NLPPlots.token_influence_histogram_segments,
            dict(
                highlight_token=token_widget,
                class_id=class_widget,
                segment_1=segment_1_widget,
                segment_2=segment_2_widget,
                num_segments=fixed(NUM_SEGMENTS),
                influences_dict=fixed(influences_dict),
                empty_message=fixed(empty_message),
                qoi_type=fixed(qoi_type),
                on_bin_change=fixed([update_influence_range]),
                on_bin_click=fixed([update_influence_value])
            )
        )

        infl_examples = widgets.interactive_output(
            NLPPlots.influence_examples_segments,
            dict(
                highlight_token=token_widget,
                influences_dict=fixed(influences_dict),
                influences_df=fixed(influences_df),
                error_driver_group_dict=fixed(error_driver_group_dict),
                influence_range=influence_range_examples_widget,
                token_frequency=fixed(token_frequency),
                group=fixed('All'),
                class_idx=class_widget
                if class_widget is not None else fixed(0)
            )
        )

        options_display = VBox(
            [
                token_widget, segment_1_widget, segment_2_widget,
                infl_examples_options
            ]
        )
        graph_display = VBox([HBox([infl_hist]), infl_examples])
        display(VBox([options_display, graph_display]))

    @check_ipython
    @check_ipywidgets
    @about(
        html=
        "Find the tokens that the model uses the most. Influence mean is used to tell a token's affinity towards a class. \
        Influence standard deviation is used to tell that a model uses the token in more complex ways. </br></br>\
        A scatter plot is provided to find tokens with high influence and high counts. Click or type a token or to see its influence distributions.</br></br>\
        You can also click the distribution to see examples in the distribution bucket range."
    )
    def global_token_summary(
        self,
        artifacts_container: ArtifactsContainer,
        num_records=None,
        max_words_to_track=500,
        offset=0,
        token_type=TokenType.WORD
    ):
        num_records = self.get_num_records(artifacts_container)
        num_classes = self.aiq.model.get_num_classes(artifacts_container)

        # Influence data
        error_driver_group_dict = self.aiq.global_explanations_error_driver_info(
            artifacts_container,
            num_records,
            max_words_to_track,
            offset=offset,
            token_type=token_type
        )

        influences_df = self.aiq.model.get_artifacts_df(
            artifacts_container,
            token_type=token_type,
            num_records=num_records,
            offset=offset
        )

        # Plot Tabs
        tab_widget = widgets.ToggleButtons(
            options=['Scatter', 'Table View'],
            description='Display:',
            disabled=False,
            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
            style=WIDGET_STYLE
        )

        # Token Plot Widget Options
        occurrence_range_widget = self.get_exp_range_widget_options(
            min_val=1,
            max_val=max(error_driver_group_dict['All']['occurrences']),
            num_nodes=40,
            first_tick=0
        )

        group_widget = widgets.Dropdown(
            options=list(error_driver_group_dict.keys()),
            value='All',
            description='Error Group:',
        )

        influence_type_widget = widgets.RadioButtons(
            options=['classes', 'predicted class vs rest'],
            value='classes',
            rows=2,
            description='Influence type:',
            style=WIDGET_STYLE,
            disabled=False
        )

        influence_range_widget = self.get_influence_range_widget(
            artifacts_container, token_type, num_records, offset
        )

        xaxis_widget = widgets.RadioButtons(
            options=['mean', 'stdev'],
            value='mean',
            description='Infl Metric:',
        )

        token_plot_options = widgets.VBox(
            [
                tab_widget,
                widgets.HBox(
                    [group_widget, xaxis_widget, influence_type_widget]
                ),
                widgets.HBox(
                    [
                        widgets.Label("Absolute Influence Filter"),
                        influence_range_widget
                    ]
                ),
                widgets.HBox(
                    [
                        widgets.Label("Sentence Occurrence Filter"),
                        occurrence_range_widget
                    ]
                )
            ]
        )

        # Histogram Widget Options
        text_widget = widgets.Text(
            description='Token:',
            value='',
            placeholder='Type something',
            continuous_update=False
        )
        infl_hist_options = widgets.HBox([text_widget])

        # Examples Widget Options
        influence_range_examples_widget = self.get_influence_range_examples_widget(
        )
        class_widget = self.get_class_widget(num_classes)

        infl_examples_options = widgets.HBox(
            [influence_range_examples_widget, class_widget]
        )

        # Update callbacks
        def update_influence_range(
            min: float, max: float, num_steps: int = 40
        ) -> None:
            """ Update the total max and min of influences on the influence range selector. This happens when a new token is clicked.

            Args:
                min (float): The new min
                max (float): The new max
            """
            # Temporary set the max as highest to allow min to not exceed max on assignment
            influence_range_examples_widget.max = sys.float_info.max
            influence_range_examples_widget.min = min
            influence_range_examples_widget.max = max
            influence_range_examples_widget.step = (max - min) / num_steps

        def update_text_widget(token):
            if text_widget.value != token:
                # when token is clicked
                text_widget.value = token

        def update_influence_value(min, max, class_idx=0):
            influence_range_examples_widget.value = [min, max]
            if class_widget is not None:
                class_widget.value = class_idx

        # Token Plot Widget
        token_plot = widgets.interactive_output(
            NLPPlots.token_influence_plot,
            dict(
                num_classes=fixed(num_classes),
                influence_type=influence_type_widget,
                plot_type=tab_widget,
                group=group_widget,
                xaxis=xaxis_widget,
                influence_range=influence_range_widget,
                occurrence_range=occurrence_range_widget,
                error_driver_group_dict=fixed(error_driver_group_dict),
                on_token_click=fixed([update_text_widget])
            )
        )
        token_plot_widget = VBox([token_plot_options, token_plot])

        # Histogram Widget
        infl_hist = widgets.interactive_output(
            NLPPlots.token_influence_histogram,
            dict(
                highlight_token=text_widget,
                num_classes=fixed(num_classes),
                group=group_widget,
                error_driver_group_dict=fixed(error_driver_group_dict),
                on_bin_change=fixed([update_influence_range]),
                on_bin_click=fixed([update_influence_value])
            )
        )
        infl_hist.layout.object_position = 'center bottom'
        infl_hist_widget = VBox([infl_hist_options, infl_hist])

        # Influence Examples Widget
        infl_examples = widgets.interactive_output(
            NLPPlots.influence_examples,
            dict(
                highlight_token=text_widget,
                group=group_widget,
                error_driver_group_dict=fixed(error_driver_group_dict),
                influences_df=fixed(influences_df),
                influence_range=influence_range_examples_widget,
                class_idx=class_widget
                if class_widget is not None else fixed(0)
            )
        )
        infl_examples_widget = VBox([infl_examples_options, infl_examples])
        # Putting it all together
        graph_display = VBox(
            [token_plot_widget, infl_hist_widget, infl_examples_widget]
        )

        display(graph_display)

    @check_ipython
    @check_ipywidgets
    @about(
        html=
        "Compare the influence distributions of two tokens to see if the model uses them differently. </br></br>\
        The model robustness widget can help find tokens that cause the model to make mistakes."
    )
    def token_influence_comparison(
        self,
        artifacts_container: ArtifactsContainer,
        num_records=None,
        max_words_to_track=500,
        offset=0,
        token_type=TokenType.WORD
    ):
        if num_records is None:
            num_records = self.aiq.model.get_default_num_records(
                artifacts_container
            )
        token_widget = self.get_token_widget()
        token2_widget = self.get_token_widget()
        empty_message = 'No instances of that token in the current split.'
        error_driver_group_dict = self.aiq.global_explanations_error_driver_info(
            artifacts_container,
            num_records,
            max_words_to_track,
            offset=offset,
            token_type=token_type
        )
        num_classes = self.aiq.model.get_num_classes(artifacts_container)

        infl_hist = self.get_infl_histogram_widget(
            token_widget, num_classes, error_driver_group_dict, empty_message
        )
        infl2_hist = self.get_infl_histogram_widget(
            token2_widget, num_classes, error_driver_group_dict, empty_message
        )

        display(
            VBox([token_widget, token2_widget,
                  HBox([infl_hist, infl2_hist])])
        )

    def gradient_landscape(
        self,
        artifacts_container: ArtifactsContainer,
        num_record,
        offset=0,
    ) -> None:
        sentence_info = self.aiq.gradient_landscape_info(
            artifacts_container, num_record, offset=offset
        )
        idxs = sentence_info.keys()
        idx_widget = widgets.Dropdown(
            options=idxs,
            value=min(idxs),
            description='Example: ',
            disabled=False,
        )
        interact(
            NLPPlots.gradient_landscape_graph,
            sentence_info=fixed(sentence_info),
            sentence_idx=idx_widget
        )

    @check_ipython
    @check_ipywidgets
    @about(html="stuff")
    def segment_output_metrics_tab(
        self,
        artifacts_container: ArtifactsContainer,
    ):
        """
        display the influence profile plot of each validation set sentence in each split
        """

        multi_class_segment_metrics = self.aiq.segment_output_metrics_info(
            artifacts_container
        )

        num_classes = len(
            multi_class_segment_metrics['total']['confusion_matrix']
            ['confusion_matrix']
        )

        widgets.Dropdown.value.tag(sync=True)
        segment_1_widget = self.get_dropdown_widget(
            multi_class_segment_metrics, value='total', description='Segment 1'
        )
        widgets.Dropdown.value.tag(sync=True)
        segment_2_widget = self.get_dropdown_widget(
            multi_class_segment_metrics, value='total', description='Segment 2'
        )

        metric_viz_widget = widgets.ToggleButtons(
            options=[
                "CONF_MATRIX", "CONF_RATES", "ACCURACY", "F1_SCORE",
                "DISADV RANKINGS"
            ],
            description='Metric:',
            disabled=False,
            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
            style=WIDGET_STYLE
        )

        output_type_widget = widgets.ToggleButtons(
            options=["Multi-Class", "Binary"],
            description='Output Type:',
            disabled=False,
            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
            style=WIDGET_STYLE
        )

        positive_group_widget = widgets.SelectMultiple(
            options=list(range(num_classes)),
            description='Positive Class IDs:',
            disabled=False,
            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
            style=WIDGET_STYLE
        )

        display_disadvantaged_segments_widget = widgets.IntSlider(
            value=0,
            min=0,
            max=len(list(multi_class_segment_metrics.keys())),
            description='Num Ranks:',
            disabled=False,
            orientation='horizontal',
            readout=True,
        )

        interact(
            NLPPlots.segment_output_metrics,
            artifacts_container=fixed(artifacts_container),
            aiq=fixed(self.aiq),
            multi_class_segment_metrics=fixed(multi_class_segment_metrics),
            metric_viz_tab=metric_viz_widget,
            output_type_tab=output_type_widget,
            positive_group_tab=positive_group_widget,
            display_disadvantaged_segments_tab=
            display_disadvantaged_segments_widget,
            segment_1=segment_1_widget,
            segment_2=segment_2_widget,
        )

    @check_ipython
    @check_ipywidgets
    @about(
        html="Find the influences per token in a sentence.</br></br>\
    You can also explore feature interactions via n-grams. The n-grams are found using correlations of gradients under different contexts."
    )
    def record_explanations_attribution_tab(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int = None,
        token_type: TokenType = TokenType.TOKEN
    ) -> None:
        """
        display the influence profile plot of each validation set sentence in each split
        
        Args:
            artifacts_container (ArtifactsContainer): Contains the metadata about the artifacts
            num_records (int, optional): Number of records to return. Defaults to None.
            token_type (TokenType, optional): The type of token aggregation. TokenType.TOKEN returns the tokenizer type. 
                TokenType.WORD tries to keep attributions to the original word in text. Defaults to TokenType.TOKEN.
        """
        if num_records is None:
            num_records = self.aiq.model.get_default_num_records(
                artifacts_container
            )

        # Get influences DF
        influences_df = self.aiq.get_influences_df(
            artifacts_container, token_type=token_type, num_records=num_records
        )

        # Control Widgets
        ## Record ID option
        records = sorted(
            list(zip(influences_df.original_index, influences_df.data_index)),
            key=lambda x: x[0]
        )
        record_id_widget = record_id_nav(records)

        # Segment options
        disable_segments = False
        segment_to_point_ids = None
        segment_widget_options = ["None"]
        try:
            segment_to_point_ids = self.aiq.model.get_segment_name_to_point_id_dict(
                artifacts_container
            )
            segment_widget_options = segment_widget_options + list(
                segment_to_point_ids.keys()
            )

        except FileNotFoundError:
            self.logger.warning(
                "Segment files not generated or found. Segments widget will be unavailable."
            )
            disable_segments = True

        segment_widget = widgets.Dropdown(
            options=segment_widget_options,
            value=segment_widget_options[0],
            description='Segment:',
            disabled=disable_segments
        )

        # QoI Option
        qoi_type_widget_options = QoIType.CLASS_WISE.get_qoi_type_widget_options(
            self.aiq.model.get_num_classes(artifacts_container)
        )
        qoi_class_widget = widgets.Dropdown(
            options=qoi_type_widget_options,
            value=qoi_type_widget_options[0],
            description='Quantity of Interest:',
            disabled=False,
            style={'description_width': 'initial'}
        )

        # Confusion Matrix option
        ## Group Ind dict
        group_ind_dict = self.aiq.model.get_group_ind_dict(
            artifacts_container, num_records
        )

        cm_widget = confusion_matrix_nav(group_ind_dict)

        def data_idxs_to_records(data_idxs):
            records = []
            for data_idx in data_idxs:
                subdf = influences_df[influences_df['data_index'] == data_idx]
                if len(subdf) > 0:
                    orig_idx = int(subdf.iloc[0].original_index)
                    records.append((orig_idx, int(data_idx)))
            records.sort(key=lambda x: x[0])
            return records

        dlink(
            (cm_widget, "value"), (record_id_widget, "records"),
            transform=data_idxs_to_records
        )

        # Tabs
        tab_widget = widgets.ToggleButtons(
            options=['Record Explanations', 'Feature Interactions'],
            description='Explanation:',
            disabled=False,
            button_style='',
            style=WIDGET_STYLE
        )

        def _record_id_row(record_id):
            return influences_df[influences_df['data_index'] == record_id
                                ].iloc[0]

        # Clicked token selector
        # NOTE: Need to keep separate widgets since
        tokens = _record_id_row(record_id_widget.value).tokens
        selected_token_widget = RecordTokenIDSelector(
            options=[(tok, i) for i, tok in enumerate(tokens)] + [("None", -1)],
            value=-1,
            description='Token:'
        )
        selected_token_widget.layout.visibility = 'hidden'

        def handle_record_id_update(change):
            record_id = change['new']
            tokens = [] if record_id == -1 else _record_id_row(record_id).tokens
            selected_token_widget.options = [
                (tok, i) for i, tok in enumerate(tokens)
            ] + [("None", -1)]
            selected_token_widget.value = -1

        def handle_qoi_update(change):
            selected_token_widget.ngram_row_idx = -1
            selected_token_widget.ngram_token_idxs = []

        def handle_ngram_table_select(row):
            selected_token_widget.value = int(row.source_token_idx)
            selected_token_widget.ngram_row_idx = int(row.name)
            selected_token_widget.ngram_token_idxs = row.token_idxs

        def barplot_update_token(token_idx):
            selected_token_widget.value = token_idx
            selected_token_widget.ngram_row_idx = -1
            selected_token_widget.ngram_token_idxs = []

        def handle_tab_update(change):
            new_tab = change['new']
            if new_tab == "Record Explanations":
                selected_token_widget.layout.visibility = 'hidden'
            else:
                selected_token_widget.layout.visibility = "visible"

        def handle_selected_token_update(_):
            # clear prev token update
            selected_token_widget.ngram_row_idx = -1
            selected_token_widget.ngram_token_idxs = []

        def update_selected_token_options(token_idxs):
            record_id = record_id_widget.value
            tokens = [] if record_id == -1 else _record_id_row(record_id).tokens
            selected_token_widget.options = [
                (tokens[i], i) for i in token_idxs
            ] + [("None", -1)]

        tab_widget.observe(handle_tab_update, names='value')
        qoi_class_widget.observe(handle_qoi_update, names='value')
        record_id_widget.observe(handle_record_id_update, names='value')
        selected_token_widget.observe(
            handle_selected_token_update, names='value'
        )

        general_widget_options = VBox(
            [
                tab_widget, record_id_widget, segment_widget, qoi_class_widget,
                cm_widget, selected_token_widget
            ]
        )

        # grad landscape line chart
        record_visualizations = interactive_output_override(
            NLPPlots.record_explanations_attribution,
            dict(
                artifacts_container=fixed(artifacts_container),
                aiq=fixed(self.aiq),
                token_type=fixed(token_type),
                segment_to_point_ids=fixed(segment_to_point_ids),
                tab=tab_widget,
                record_id=record_id_widget,
                segment=segment_widget,
                group_idxs=cm_widget,
                group_name=(cm_widget, 'group_name'),
                qoi_class=qoi_class_widget,
                selected_token_idx=selected_token_widget,
                selected_ngram_token_idxs=(
                    selected_token_widget, 'ngram_token_idxs'
                ),
                selected_ngram_row_idx=(selected_token_widget, 'ngram_row_idx'),
                influences_df=fixed(influences_df),
                update_selected_token=fixed(handle_ngram_table_select),
                update_selected_token_options=fixed(
                    update_selected_token_options
                ),
                barplot_update_token=fixed(barplot_update_token)
            )
        )

        display(VBox([general_widget_options, record_visualizations]))

    @check_ipython
    @check_ipywidgets
    @about(
        html=
        "This widget is used to explore data issues. You can see the examples that contain a token by class and with explanations. It is recommended to analyze the training split"
    )
    def data_exploration_tab(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int = None,
        max_influence_examples_per_token: int = 10,
        num_train_examples_per_token: int = 5,
        max_words_to_track: int = 500,
        offset: int = 0,
        token_type: TokenType = TokenType.WORD,
        ranking='occurrence'
    ):
        """Explore the data in a split. Can surface data imbalance, or see how sentences are explained while grouping together examples from label classes.

        Args:
            artifacts_container (ArtifactsContainer): The artifacts metadata.
            num_records (int, optional): the number of records to take. Defaults to None.
            max_influence_examples_per_token (int, optional): The number of examples to show explanations for. Defaults to 10.
            num_train_examples_per_token (int, optional): The number of examples per class to show. Defaults to 5.
            max_words_to_track (int, optional): The number of tokens. Defaults to 500.
            offset (int, optional): the starting offset of the records to take. Defaults to 0.
            token_type (TokenType, optional): The token type. Defaults to TokenType.WORD.
            ranking (str, optional): The sort. Defaults to 'occurrence'.
        """
        if num_records is None:
            num_records = self.aiq.model.get_default_num_records(
                artifacts_container
            )

        ind_widget = widgets.BoundedIntText(
            value=0,
            min=0,
            max=num_records,
            step=1,
            description='Number:',
            disabled=False
        )
        widgets.Dropdown.value.tag(sync=True)

        qoi_type_widget_options = QoIType.CLASS_WISE.get_qoi_type_widget_options(
            self.aiq.model.get_num_classes(artifacts_container)
        )
        qoi_class_widget = widgets.Dropdown(
            options=qoi_type_widget_options,
            value=qoi_type_widget_options[0],
            description='QoI:',
            disabled=False,
        )

        error_driver_group_dict = self.aiq.global_explanations_error_driver_info(
            artifacts_container,
            num_records,
            max_words_to_track,
            offset=offset,
            token_type=token_type,
            ranking=ranking
        )
        group_widget = widgets.Dropdown(
            options=list(error_driver_group_dict.keys()),
            value='All',
            description='Error Group:',
            disabled=False,
        )
        all_tokens = list(error_driver_group_dict['All'].tokens)
        text_examples_df_train_classes = self.aiq.model.get_text_examples_df(
            artifacts_container, num_records, all_tokens,
            num_train_examples_per_token, token_type
        )
        record_influences_df_dict = self.aiq.model.get_artifacts_df(
            artifacts_container,
            token_type=token_type,
            num_records=num_records,
            offset=offset
        )

        def dropdown_eventhandler(change):
            text_widget.value = error_driver_group_dict[
                group_widget.value].iloc[ind_widget.value].tokens

        text_widget = widgets.Text(
            value=error_driver_group_dict['All'].iloc[0].tokens,
            placeholder='Type something',
            description='Token:',
            disabled=False,
            continuous_update=False
        )
        ind_widget.observe(dropdown_eventhandler, names='value')
        group_widget.observe(dropdown_eventhandler, names='value')

        interact(
            NLPPlots.global_explanations_error_driver,
            token=text_widget,
            group=group_widget,
            token_ind_group=ind_widget,
            qoi_class=qoi_class_widget,
            max_influence_examples_per_token=fixed(
                max_influence_examples_per_token
            ),
            record_influences_df_dict=fixed(record_influences_df_dict),
            error_driver_group_dict=fixed(error_driver_group_dict),
            text_examples_df_train_classes=fixed(
                text_examples_df_train_classes
            )
        )

    @check_ipython
    @check_ipywidgets
    @about(
        html=
        "Analyze model robustness by seeing if synonym word swaps cause the model to change it's output. \
        If word swaps do not change the meaning, but the model changes it's output, this is a model robustness issue.</br></br>\
        Word swaps are found using a masked language model (MLM). The best candidates are chosen using coherence scores as some replacements may not make sense. </br>ex) 'I thank you' vs 'I thanks you'"
    )
    def model_robustness_analysis_tab(
        self,
        artifacts_container: ArtifactsContainer,
        artifacts_container_cf: ArtifactsContainer,
        num_records=None,
        num_records_cf=None,
        offset=0,
        token_type: str = TokenType.TOKEN
    ) -> None:
        """ Widget to show model robustness to perturbation.

        Args:
            artifacts_container (ArtifactsContainer): The metadata of the original data.
            artifacts_container_cf (ArtifactsContainer): The metadata of examples with counterfactual perturbations.
            num_records (int, optional): The number of records to create counterfactuals from. Defaults to None.
            num_records_cf (int, optional): The number of counterfactuals to show. Defaults to None.
            offset: The starting offset of records to show. Defaults to 0.
            token_type: Influence aggregation on tokens or owrds. Defaults to TokenType.TOKEN.
        """
        if num_records is None:
            num_records = self.aiq.model.get_default_num_records(
                artifacts_container
            )
        if num_records_cf is None:
            num_records_cf = self.aiq.model.get_default_num_records(
                artifacts_container_cf
            )
        num_classes = self.aiq.model.get_num_classes(artifacts_container)
        accuracy_group_name_dict = get_accuracy_group_name_dict(num_classes)
        group_options = list(accuracy_group_name_dict.values()) + ['All']
        group_widget = widgets.Dropdown(
            options=group_options,
            value='All',
            description='Original Error Group:',
            disabled=False,
            style=WIDGET_STYLE
        )
        group_widget_cf = widgets.Dropdown(
            options=group_options,
            value='All',
            description='Counterfactual Error Group:',
            disabled=False,
            style=WIDGET_STYLE
        )

        display_level_widget = widgets.Dropdown(
            options=['global', 'local'],
            value='global',
            description='Local/Global:',
            disabled=False,
            style=WIDGET_STYLE
        )
        qoi_type_widget_options = QoIType.CLASS_WISE.get_qoi_type_widget_options(
            self.aiq.model.get_num_classes(artifacts_container)
        )
        qoi_class_widget = widgets.Dropdown(
            options=qoi_type_widget_options,
            value=qoi_type_widget_options[0],
            description='QoI:',
            disabled=False,
            style=WIDGET_STYLE
        )
        ind_widget = widgets.Dropdown(
            options=np.arange(num_records_cf),
            value=0,
            description='Example: ',
            disabled=False,
            style=WIDGET_STYLE
        )

        word_from_filter_widget = widgets.Text(
            description='Word From Selection:',
            value='',
            placeholder='leave blank for selecting all words',
            style=WIDGET_STYLE,
            continuous_update=False
        )
        word_to_filter_widget = widgets.Text(
            description='Word To Selection:',
            value='',
            placeholder='leave blank for selecting all words',
            style=WIDGET_STYLE,
            continuous_update=False
        )

        text_df = self.aiq.model_robustness_info(
            artifacts_container,
            artifacts_container_cf,
            num_records=num_records,
            num_records_cf=num_records_cf,
            offset=offset,
            token_type=token_type
        )

        if text_df is None:
            return

        text_df = text_df.sort_values(by=['coherence_score'], ascending=False)

        page_size = 50

        n_pages = math.ceil(len(text_df) / page_size)
        page_idx = widgets.BoundedIntText(
            value=1,
            min=1,
            max=n_pages,
            step=1,
            disabled=n_pages == 1,
            description='Page #:',
            style=WIDGET_STYLE
        )

        def update_ind_widget_options(*args):
            filters = NLPPlots.get_counterfactual_filters(
                text_df, group_widget.value, group_widget_cf.value,
                word_from_filter_widget.value, word_to_filter_widget.value
            )
            ind_widget.options = np.where(filters)[0]

        update_ind_widget_options()
        ind_widget.observe(update_ind_widget_options)
        group_widget.observe(update_ind_widget_options)
        group_widget_cf.observe(update_ind_widget_options)
        word_from_filter_widget.observe(update_ind_widget_options)
        word_to_filter_widget.observe(update_ind_widget_options)

        interact(
            NLPPlots.display_counterfactual_text_df,
            text_df=fixed(text_df),
            display_level=display_level_widget,
            page_size=fixed(page_size),
            page_idx=page_idx,
            word_from=word_from_filter_widget,
            word_to=word_to_filter_widget,
            qoi_class=qoi_class_widget,
            ind_group=ind_widget,
            group=group_widget,
            group_cf=group_widget_cf
        )

    @check_ipython
    @check_ipywidgets
    @about(
        html=
        "Evaluate new sentences on the model. This is useful for hypothesis testing. </br></br>\
        It is recommended to test hypothesis about token swaps because the model robustness widget only tests examples in the distribution of the original data."
    )
    def evaluate_text_tab(
        self, artifacts_container: ArtifactsContainer,
        model_wrapper: nlp.Wrappers.ModelRunWrapper, model: Any,
        tokenizer: nlp.Wrappers.TokenizerWrapper
    ) -> None:
        """
        Evaluate the model on user provided inputs
        """
        text_widget = widgets.Textarea(
            value='',
            placeholder='Type something',
            description='Sentence:',
            disabled=False,
            continuous_update=False
        )
        button = widgets.Button(description="Evaluate")

        num_classes = self.aiq.model.get_num_classes(artifacts_container)
        class_names = [
            'class_{}'.format(cl) for cl in range(num_classes)
        ]  ## TODO: add task-appropriate class-name modules
        NLPPlots.evaluate_text_box(
            button, model_wrapper, model, tokenizer, text_widget, class_names
        )
