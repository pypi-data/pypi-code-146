from p3ui import *


class ListView(ScrolledColumn):
    """ WIP: POC, do not use this """

    def __init__(self, *, delegate=None, delegate_init=None, model=None, on_change=None):
        super().__init__()
        self.on_change = on_change
        self._model = model
        self._delegate = delegate
        self._delegate_init = delegate_init
        self._init()

    def _init(self):
        self.clear()
        if self._model is None:
            self._repeater = None
            return
        if self._delegate is None:
            self._repeater = None
            return
        self._repeater = Repeater(target_container=self, delegate=self._delegate, delegate_init=self._delegate_init)
        self.update()

    def update(self):
        if self._repeater is None:
            return
        self._repeater.eval(self._model)
        self.eval()

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self._model = model
        self._init()

    @property
    def delegate(self):
        return self._delegate

    @delegate.setter
    def delegate(self, delegate):
        self._delegate = lambda: Row(
            padding=(0 | px, 0 | px),
            content=delegate()
        )
        self._init()

    @property
    def delegate_init(self):
        return self._delegate_init

    @delegate.setter
    def delegate_init(self, delegate_init):
        self._delegate_init = lambda index, item, delegate: delegate_init(index, item, delegate.content)
        self._init()

    @property
    def selected_index(self):
        return -1

    @property
    def selected_item(self):
        return None

    @property
    def active_index(self):
        return -1

    @property
    def active_item(self):
        return None

    def eval(self):
        if self._repeater is None:
            return
        model.index = 0
        for item, child in zip(self.model, self.children):
            if child.visible:
                model.item = item
                child.eval()
                model.index += 1
