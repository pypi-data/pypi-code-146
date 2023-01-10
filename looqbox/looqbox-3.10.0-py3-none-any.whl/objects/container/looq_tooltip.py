from looqbox.objects.container.abstract_container import AbstractContainer
from looqbox.render.abstract_render import BaseRender


class ObjTooltip(AbstractContainer):

    def __init__(self, *children, text, **properties):
        """
        :param children: Children to be contained.
        :param text: Text to be displayed on mouse hover.
        :param properties: properties derived from parent:  --value
                                                            --render_condition
                                                            --tab_label
                                                            --css_options
        """
        super().__init__(*children, **properties)
        self.text = text
        self.orientation = "top"

    def to_json_structure(self, visitor: BaseRender):
        return visitor.tooltip_render(self)

    @property
    def set_orientation_top(self):
        self.orientation = "top"
        return self

    @property
    def set_orientation_right(self):
        self.orientation = "right"
        return self

    @property
    def set_orientation_bottom(self):
        self.orientation = "bottom"
        return self

    @property
    def set_orientation_left(self):
        self.orientation = "left"
        return self

    @property
    def set_orientation_top_left(self):
        self.orientation = "topLeft"
        return self

    @property
    def set_orientation_top_right(self):
        self.orientation = "topRight"
        return self

    @property
    def set_orientation_bottom_left(self):
        self.orientation = "bottomLeft"
        return self

    @property
    def set_orientation_bottom_right(self):
        self.orientation = "bottomRight"
        return self

    @property
    def set_orientation_left_top(self):
        self.orientation = "leftTop"
        return self

    @property
    def set_orientation_left_bottom(self):
        self.orientation = "leftBottom"
        return self

    @property
    def set_orientation_right_top(self):
        self.orientation = "rightTop"
        return self

    @property
    def set_orientation_right_bottom(self):
        self.orientation = "rightBottom"
        return self
