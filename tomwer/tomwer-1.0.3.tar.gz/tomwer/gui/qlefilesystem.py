from silx.gui import qt


class QLFileSystem(qt.QLineEdit):
    def __init__(self, text, parent, filters=None, **kwargs):
        super().__init__(parent=parent, **kwargs)
        self.completer = qt.QCompleter()
        model = qt.QDirModel(self.completer)
        if filters is not None:
            model.setFilter(filters)
        self.completer.setModel(model)
        self.setCompleter(self.completer)
