from PySide6.QtCore import QObject, QRunnable, Signal


class Generator(QRunnable):
    """
    A class that runs a task in a separate thread and emits signals to indicate its status.

    Args:
        task (callable): A callable that takes two arguments, generationList and proxyID, 
            and returns data.
        generationList (list): A list of items to be processed by the task.
        proxyID (int): An ID associated with the task.

    """
    class GeneratorSignals(QObject):
        """
        A class that defines the signals that the Generator class can emit.

        Signals:
            dataGenerated: Emitted when data is generated. Passes a list of data.
            error: Emitted when an error occurs. Passes a string representing the error.
            finished: Emitted when the task is finished, whether it succeeded or failed.
        """
        dataGenerated = Signal(list)
        error = Signal(str)
        finished = Signal()

    def __init__(self, task, generationList: list, proxyID: int):
        super().__init__()
        self.signals = self.GeneratorSignals()
        self.task = task
        self.generationList = generationList
        self.proxyID = proxyID

    def run(self):
        """
        Executes the task, emits the dataGenerated signal if successful, 
        emits the error signal if an error occurs, and emits the finished signal when done.
        """
        try:
            data = self.task(self.generationList, self.proxyID)
            self.signals.dataGenerated.emit(data)
        except Exception as e:
            self.signals.error.emit(str(e))
        self.signals.finished.emit()
