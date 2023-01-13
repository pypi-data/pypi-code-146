from looqbox.objects.component_utility.css import Css


class LayoutCss(Css):
    def __init__(self, name, value):
        super().__init__(name, value)

    def top(self, value):
        return LayoutCss(self.property + "Top", value)

    def left(self, value):
        return LayoutCss(self.property + "Left", value)

    def right(self, value):
        return LayoutCss(self.property + "Right", value)

    def bottom(self, value):
        return LayoutCss(self.property + "Bottom", value)
