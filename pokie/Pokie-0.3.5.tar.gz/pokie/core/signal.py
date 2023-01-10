import signal
from rick.mixin import Injectable
from rick.base import Di


class SignalManager(Injectable):
    def __init__(self, di: Di):
        super().__init__(di)
        self.handlers = {}

    def add_handler(self, signalnum: int, handler: callable):
        assert callable(handler) is True
        assert isinstance(signalnum, int)

        if signalnum in self.handlers.keys():
            self.handlers[signalnum].append(handler)
        else:
            self.handlers[signalnum] = [handler]
            self._register_handler(signalnum)

    def _register_handler(self, signalnum: int):
        def wrap_signal(signal_no, stack_frame):
            for handler in self.handlers[signal_no]:
                handler(self.get_di(), signal_no, stack_frame)

        signal.signal(signalnum, wrap_signal)
