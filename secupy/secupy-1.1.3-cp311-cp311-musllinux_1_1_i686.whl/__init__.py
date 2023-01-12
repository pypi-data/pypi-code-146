import _secupy


def __getattr__(name):
    if hasattr(_secupy, name):
        return getattr(_secupy, name)
    raise AttributeError(f"module {__name__} has no attribute {name}")
