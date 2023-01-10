from looqbox.objects.component_utility.css import Css


class FlexCss(Css):
    def __init__(self, name, value):
        super().__init__(name, value)

    @property
    def row(self):
        return FlexCss(self.property, 'row')

    @property
    def column(self):
        return FlexCss(self.property, 'column')
