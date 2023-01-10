from looqbox.objects.component_utility.css import Css


class PositionalCss(Css):
    def __init__(self, name, value):
        super().__init__(name, value)

    @property
    def flex_start(self):
        return PositionalCss(self.property, 'flex-start')

    @property
    def center(self):
        return PositionalCss(self.property, 'center')

    @property
    def flex_end(self):
        return PositionalCss(self.property, 'flex-end')

    @property
    def space_around(self):
        return PositionalCss(self.property, 'space-around')

    @property
    def space_between(self):
        return PositionalCss(self.property, 'space-between')

    @property
    def space_evenly(self):
        return PositionalCss(self.property, 'space-evenly')

    @property
    def stretch(self):
        return PositionalCss(self.property, 'stretch')
