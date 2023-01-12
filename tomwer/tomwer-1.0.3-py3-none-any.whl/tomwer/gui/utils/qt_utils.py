from contextlib import contextmanager
from silx.gui import qt


@contextmanager
def block_signals(w: qt.QWidget):
    old = w.blockSignals(True)
    try:
        yield
    finally:
        w.blockSignals(old)
