from spy.vm.objects import W_Root
from spy.vm import wt


class W_Primitive(W_Root):

    def __init__(self, wt_value, value):
        # we should add proper error reporting, but for now it's fine
        assert wt_value == wt.i32
        assert isinstance(value, int)
        self.wt_value = wt_value
        self.value = value

    def unwrap(self):
        return self.wt_value, self.value
