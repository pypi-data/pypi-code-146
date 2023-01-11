from ..util.Logger import classLogger


class MissingOption(Exception):
    pass


@classLogger
class Optionizable:
    options = {}

    def __init__(self, options={}):
        self.options = self.initialOptions()

        for _, val in enumerate(options):
            self.options[val] = options[val]

    def getOption(self, name):
        if not name in self.options:
            raise MissingOption("The option '" + name + "' is missing")

        return self.options[name]

    def initialOptions(self, defaultOptions=None):
        return {}
