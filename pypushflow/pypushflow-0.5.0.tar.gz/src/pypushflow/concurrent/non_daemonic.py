import sys
from multiprocessing import context


def get_context(context: str = None) -> context.BaseContext:
    return _NONDAEMONIC_CONTEXTS[context]()


class SpawnNonDaemonicProcess(context.SpawnProcess):
    @property
    def daemon(self):
        return False

    @daemon.setter
    def daemon(self, value):
        pass


class SpawnNonDaemonicContext(context.SpawnContext):
    Process = SpawnNonDaemonicProcess


if sys.platform == "win32":
    _NONDAEMONIC_CONTEXTS = {
        None: SpawnNonDaemonicContext,
        "spawn": SpawnNonDaemonicContext,
    }
else:

    class ForkNonDaemonicProcess(context.ForkProcess):
        @property
        def daemon(self):
            return False

        @daemon.setter
        def daemon(self, value):
            pass

    class ForkServerNonDaemonicProcess(context.ForkServerProcess):
        @property
        def daemon(self):
            return False

        @daemon.setter
        def daemon(self, value):
            pass

    class ForkNonDaemonicContext(context.ForkContext):
        Process = ForkNonDaemonicProcess

    class ForkServerNonDaemonicContext(context.ForkServerContext):
        Process = ForkServerNonDaemonicProcess

    if sys.platform == "darwin":
        _NONDAEMONIC_CONTEXTS = {
            None: SpawnNonDaemonicContext,
            "spawn": SpawnNonDaemonicContext,
            "fork": ForkNonDaemonicContext,
            "forkserver": ForkServerNonDaemonicContext,
        }
    else:
        _NONDAEMONIC_CONTEXTS = {
            None: ForkNonDaemonicContext,
            "spawn": SpawnNonDaemonicContext,
            "fork": ForkNonDaemonicContext,
            "forkserver": ForkServerNonDaemonicContext,
        }
