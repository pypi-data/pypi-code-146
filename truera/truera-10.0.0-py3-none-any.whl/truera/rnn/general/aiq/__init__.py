from truera.rnn.general.container.model import ModelProxy


class AIQ(object):

    def __init__(self, model: ModelProxy):
        self.model = model