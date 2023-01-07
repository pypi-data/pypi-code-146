from tests.plugins.plugin1.api import IFirstInterface


class Foo(IFirstInterface):
    def first_method(self):
        return "first"
