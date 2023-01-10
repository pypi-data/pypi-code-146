from looqbox.objects.visual.shape.looq_shape import ObjShape
from looqbox.render.abstract_render import BaseRender
from looqbox.objects.component_utility.css_option import CssOption as css


class ObjLine(ObjShape):
    def __init__(self, **properties):
        super().__init__(**properties)
        self.size = None
        self.obj_class = ["vertical"]

    def set_size(self, value):
        self.size = value
        self._update_size()
        return self

    def _update_size(self):
        self._clear_size_options()
        if self.size is not None:
            _size_options = {
                "vertical": css.Height,
                "horizontal": css.Width
            }
            css_var = _size_options.get(self.obj_class[0])
            self.css_options = css.add(self.css_options, css_var(self.size))

    @property
    def set_orientation_horizontal(self):
        self.obj_class = ["horizontal"] + list(self.obj_class or [])
        self._update_size()
        return self

    @property
    def set_orientation_vertical(self):
        self.obj_class = ["vertical"] + list(self.obj_class or [])
        self._update_size()
        return self

    def set_thickness(self, value):
        self.css_options = css.add(self.css_options, css.BorderWidth(value))
        return self

    def set_color(self, value):
        self.css_options = css.add(self.css_options, css.BorderColor(value))
        return self

    def to_json_structure(self, visitor: BaseRender):
        return visitor.line_render(self)

    @property
    def set_alignment_inherit(self):
        self.css_options = css.add(self.css_options, css.AlignSelf.inherit)
        return self

    @property
    def set_alignment_center(self):
        self.css_options = css.add(self.css_options, css.AlignSelf.center)
        return self

    @property
    def set_alignment_flex_end(self):
        self.css_options = css.add(self.css_options, css.AlignSelf.flex_end)
        return self

    @property
    def set_alignment_flex_start(self):
        self.css_options = css.add(self.css_options, css.AlignSelf.flex_start)
        return self

    @property
    def set_alignment_initial(self):
        self.css_options = css.add(self.css_options, css.AlignSelf.initial)
        return self

    @property
    def set_alignment_normal(self):
        self.css_options = css.add(self.css_options, css.AlignSelf.normal)
        return self

    @property
    def set_alignment_revert(self):
        self.css_options = css.add(self.css_options, css.AlignSelf.revert)
        return self

    @property
    def set_alignment_self_end(self):
        self.css_options = css.add(self.css_options, css.AlignSelf.self_end)
        return self

    @property
    def set_alignment_self_start(self):
        self.css_options = css.add(self.css_options, css.AlignSelf.self_start)
        return self

    @property
    def set_alignment_start(self):
        self.css_options = css.add(self.css_options, css.AlignSelf.start)
        return self

    @property
    def set_alignment_stretch(self):
        self.css_options = css.add(self.css_options, css.AlignSelf.stretch)
        return self

    @property
    def set_alignment_baseline(self):
        self.css_options = css.add(self.css_options, css.AlignSelf.baseline)
        return self

    def _clear_size_options(self):
        self.css_options = css.clear(self.css_options, (css.Width, css.Height))
