import numpy as np

from looqbox.objects.visual.abstract_visual_component import AbstractVisualComponent
from looqbox.render.abstract_render import BaseRender


class ObjGauge(AbstractVisualComponent):
    """
    Traces are composed by a set of keys:
        :param value: The value to be displayed
        :param label: The label to be displayed within a tooltip on trace hover
        :param scale_min (Optional): Minimum value used on gauge scale - Default = 0
        :param scale_max (Optional): Maximum value used on gauge scale - Default = 1
        :param value_format (Optional): Format option to be applied on the values - Default = "percent:0"
        :param color (Optional): determines the color of each trace, must follow the constraints:
            --------------------------------------------------------
            String: #48F86E
            --------------------------------------------------------
            Dict - Gradient:
            {
                0: "#ffffff", # Color to be displayed after 0 %
                0.5: "#ffffff", # Color to be displayed after 50 %
                0.75: "#ffffff", # Color to be displayed after 75 %
            }
            --------------------------------------------------------
            Function -> The function must return a String or Dict
            Example:

            def choose_color(value):
                if value > 0.2:
                    return "#ffffff"
                return "#000000"

            def choose_gradient(value):
                if value > 0.2:
                    return {
                    0: "#ffffff",
                    50: "#000000"
                }
                return {
                    0: "#ffffff",
                    50: "#000000"
                }
            --------------------------------------------------------
    Use example:
        trace_0 = {
            value: 0.4,
            label: "Store A: 40%",
        }
        trace_1 = {
            value: 0.2,
            label: "Store B: 20%",
            color: "#48F86E"
        }
        gauge = lq.ObjGauge(trace_0, trace_1)
    """
    def __init__(self, *traces, animated=True, **properties):
        """
        :param traces: Traces are a set of dictionaries containing all gauge info.
        :param animated: Boolean to indicate if it should be animated
        :param properties: Inherited properties
        """
        super().__init__(**properties)
        self.traces = list(np.hstack(traces)) if traces else []
        self.animated = animated

    def to_json_structure(self, visitor: BaseRender):
        return visitor.gauge_render(self)
