"""
This module contains classes for the creation of a widget to display status updates
on the GUI from a calculation running in its own thread.
"""
import sys
import datetime
import traceback
from PyQt5.QtCore import (QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import (QVBoxLayout, QWidget, QPlainTextEdit)


class WorkerSignals(QObject):
      """
      Defines the signals available from a running worker thread.
      Supported signals are:
          finished - No data
          error - tuple (exctype, value, traceback.format_exc() )
          result - object data returned from processing, anything
          progress - int indicating % progress
          log - string containing the status of the calculation

      An object instanciated from this class must be passed into the 
      callback function, so that it can communicate with the GUI.
      """
      finished = pyqtSignal()
      error = pyqtSignal(tuple)
      result = pyqtSignal(object)
      progress = pyqtSignal(int)
      log = pyqtSignal(str)


class Worker(QRunnable):
      """
      This class allows a long-running calculation to run in its own thread, 
      the Worker thread, separate from the thread that the GUI is run in.

      Threads run in the same memory space, Processes run in a separate memory space.
      
      The function containing the long-running calculation is passed as an object
      into this class's object constructor.

      Thus, during the calculation, status updates can be made to the GUI without
      causing it to freeze. 

      It inherits from QRunnable to handle worker thread setup, signals and
      wrap-up.
        
      Input arguments:
      ****************
      func: The callback function containing a long-running calculation as an object. 
      args: arguments to pass to the callback function
      kwargs: Keyword arguments to pass to the callback function
      """
      def __init__(self, func, *args, **kwargs):
          super().__init__()
          self._func = func
          self.args = args
          self.signals = WorkerSignals()
          # Add the signals object to the kwargs
          kwargs["signals"] = self.signals
          self.kwargs = kwargs
          

      @pyqtSlot()
      def run(self):
          """
          Executes the function passed into the Worker object 
          and communicates messages from within this function 
          to the GUI.
          """
          try:
            result = self._func(*self.args, **self.kwargs)
          except Exception:
              traceback.print_exc()
              exctype, value = sys.exc_info()[:2]
              self.signals.error.emit((exctype, value, traceback.format_exc()))
          else:
              self.signals.result.emit(result) # Return the result of the calculation
          finally:
              self.signals.finished.emit() # Finished


class LoggingWidget(QWidget):
    """
    This class creates a custom composite widget that displays status updates
    from the callback function in a plain text textbox.  

    Additionally, it creates a thread for the callback function to run in.

    Input arguments:
    ****************
      func: The callback function containing a long-running calculation as an object. 
      args: arguments to pass to the callback function
      kwargs: Keyword arguments to pass to the callback function
    """
    def __init__(self, func, *args, **kwargs):
          super().__init__()
          self._function = func
          self.args = args
          self.kwargs = kwargs
          layout = QVBoxLayout()
          self.displayLogs = QPlainTextEdit()
          self.displayLogs.setReadOnly(True)
          layout.addWidget(self.displayLogs)
          self.setLayout(layout)
          self.threadpool = QThreadPool()
          #Comment out the next line of code if you wish to trigger
          #execution of the callback function by a button press on the GUI
          self.executeFunction()  


    def executeFunction(self):
        """
        This function sets up a Worker object to run the callback function and
        starts it running in it's own thread. 

        Additionally, it sets up communication of status from the callback function
        to the plain text textbox in the GUI thread.

        Connect this function to the  clicked() signal of a QPushButton if you wish to
        start with calculation with the click of a  button on the GUI.
        """
        worker = Worker(self._function, *self.args, **self.kwargs)
        worker.signals.log.connect(self.logProgress)
        worker.signals.result.connect(self.logResult)
        worker.signals.finished.connect(self.logFinished)
        worker.signals.progress.connect(self.logProgress)
        # Start the calculation in its own thread
        self.threadpool.start(worker)
          

    def logProgress(self, text):
        self.displayLogs.appendPlainText(str(datetime.datetime.now())[:19] + ': ' + text)


    def logResult(self, text):
        self.displayLogs.appendPlainText(str(datetime.datetime.now())[:19] + ': ' + text)


    def logFinished(self):
        self.displayLogs.appendPlainText(str(datetime.datetime.now())[:19] + ': ' + "Finished")

