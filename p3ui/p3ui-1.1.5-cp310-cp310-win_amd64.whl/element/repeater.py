import inspect

from p3ui.element.model import model


class Repeater:
    """
    add / removes elements to a target_container node, based on a model
    """
    data = None

    def __init__(self, target_container, delegate, model=None, delegate_init=None):
        target_container.clear()
        target_container.eval = self._eval
        self.target_container = target_container
        self.delegate = delegate
        self.delegate_init = delegate_init
        self._repeat_state = []

        self.model = model

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, m):
        self._model = m
        self.eval(self._model)

    def _eval(self):
        self.eval(self._model)

    def eval(self, data):
        self._model = data
        #
        # clear container if no model is set
        if data is None:
            self.target_container.clear()
            return
        #
        # support int ranges
        if isinstance(data, int):
            data = range(data)
        elif inspect.ismethod(data):
            data = data()
        elif inspect.isfunction(data):
            data = data()
        index = 0
        for item in data:
            if index < len(self._repeat_state):
                state = self._repeat_state[index]
                if state[0] != item:
                    state[0] = item
                    if self.delegate_init:
                        self.delegate_init(index, state[0], state[1])
            else:
                state = [item, self.delegate()]
                self._repeat_state.append(state)
                self.target_container.add(state[1])
                if self.delegate_init:
                    self.delegate_init(index, state[0], state[1])
            model.item = state[0]
            model.index = index
            state[1].eval()
            index += 1
        while index < len(self._repeat_state):
            self.target_container.remove(self._repeat_state[-1][1])
            self._repeat_state.pop(-1)
