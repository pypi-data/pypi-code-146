from looqbox.objects.component_utility.css import Css


class SelfPositional(Css):
    def __init__(self, name, value):
        super().__init__(name, value)

    @property
    def flex_start(self):
        return SelfPositional(self.property, 'flex-start')

    @property
    def center(self):
        return SelfPositional(self.property, 'center')

    @property
    def flex_end(self):
        return SelfPositional(self.property, 'flex-end')

    @property
    def stretch(self):
        return SelfPositional(self.property, 'stretch')

    @property
    def self_end(self):
        return SelfPositional(self.property, 'self-end')

    @property
    def self_start(self):
        return SelfPositional(self.property, 'self-start')

    @property
    def start(self):
        return SelfPositional(self.property, 'start')

    @property
    def revert(self):
        return SelfPositional(self.property, 'revert')

    @property
    def inherit(self):
        return SelfPositional(self.property, 'inherit')

    @property
    def initial(self):
        return SelfPositional(self.property, 'initial')

    @property
    def normal(self):
        return SelfPositional(self.property, 'normal')

    @property
    def baseline(self):
        return SelfPositional(self.property, 'baseline')
