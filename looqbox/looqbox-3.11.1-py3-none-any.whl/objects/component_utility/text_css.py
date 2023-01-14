from looqbox.objects.component_utility.css import Css


class TextCss(Css):
    def __init__(self, name, value):
        super().__init__(name, value)

    @property
    def left(self):
        return TextCss(self.property, 'left')

    @property
    def center(self):
        return TextCss(self.property, 'center')

    @property
    def right(self):
        return TextCss(self.property, 'right')
