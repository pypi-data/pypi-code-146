from looqbox.objects.visual.abstract_visual_component import AbstractVisualComponent
from looqbox.objects.component_utility.css_option import CssOption as css
from looqbox.render.abstract_render import BaseRender


class ObjText(AbstractVisualComponent):
    def __init__(self, text, **properties):
        super().__init__(**properties)
        self.text = text

    @property
    def set_text_alignment_left(self):
        self.css_options = css.add(self.css_options, css.TextAlign.left)
        return self

    @property
    def set_text_alignment_center(self):
        self.css_options = css.add(self.css_options, css.TextAlign.center)
        return self

    @property
    def set_text_alignment_right(self):
        self.css_options = css.add(self.css_options, css.TextAlign.right)
        return self

    def to_json_structure(self, visitor: BaseRender):
        return visitor.text_render(self)

    def __repr__(self):
        return f"ObjText({self.text})"
