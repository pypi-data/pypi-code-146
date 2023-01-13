from PySide6.QtCore import QThreadPool

class ManagedThreadPool(QThreadPool):
    """
    A thread pool that keeps track of active threads and allows for canceling them.

    Args:
        *args: Variable length argument list to be passed to QThreadPool.
        **kwargs: Arbitrary keyword arguments to be passed to QThreadPool.

    Attributes:
        activeThreads (list): A list of active threads.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.activeThreads = []
    
    def start(self, runnable):
        """
        Start a new thread and add it to the list of active threads.

        Args:
            runnable (QRunnable): The runnable to be executed by the thread.
        """
        self.activeThreads.append(runnable)
        super().start(runnable, 0)
    
    def cancel(self, runnable):
        """
        Cancel a thread, disconnecting the finished signal and removing it from the list of active threads.

        Args:
            runnable (QRunnable): The runnable to be canceled.
        """
        if runnable in self.activeThreads:
            runnable.signals.dataGenerated.disconnect()
            self.activeThreads.remove(runnable)
        else:
            print("Thread not found")
    
    def cancelAll(self):
        """
        Cancel all active threads.
        """
        for runnable in self.activeThreads:
            self.cancel(runnable)
    
    def _onRunnableFinished(self, runnable):
        """
        A slot method that is called when a thread finishes execution
        Args:
            runnable (QRunnable): The runnable that has finished execution.
        """
        if runnable in self.activeThreads:
            self.activeThreads.remove(runnable)
