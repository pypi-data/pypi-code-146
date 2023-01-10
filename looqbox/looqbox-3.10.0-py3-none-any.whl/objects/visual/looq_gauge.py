from looqbox.objects.visual.abstract_visual_component import AbstractVisualComponent
from looqbox.render.abstract_render import BaseRender


class ObjGauge(AbstractVisualComponent):
    # TODO Replace color default value and choose new name for value (parent conflict)
    def __init__(self, value, minimum=0, maximum=100, color=None, **properties):
        """
        :param value: Value inbetween limits
        :param minimum: Minimum value limit
        :param maximum: Maximum value limit
        :param color: Color scheme to be followed on gauge rendering.
        :param properties: properties derived from parent:  --value
                                                            --render_condition
                                                            --tab_label
                                                            --css_options
        """
        super().__init__(**properties)
        self.value = value
        self.minimum = minimum
        self.maximum = maximum
        self.color = color

    def to_json_structure(self, visitor: BaseRender):
        return visitor.gauge_render(self)
