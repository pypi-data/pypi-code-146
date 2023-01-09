from typing import Optional
from lcmlog.event import Event


class LogReader:
    """
    Utility class for reading LCM log file events in order. Iterable.
    """
    
    def __init__(self, filename: str):
        self._filename = filename
        
        self._f = None  # File handle
    
    @property
    def f(self):
        """
        Get the file. If not already open, open for reading.
        """
        if self._f is None:
            self._f = open(self._filename, 'rb')
        return self._f
    
    def __del__(self):
        """
        Close the file, if it exists.
        """
        if self._f is not None:
            self._f.close()
    
    def __iter__(self):
        return self
    
    def __next__(self) -> Event:
        event = self.read()
        if event is None:
            raise StopIteration
        return event
    
    def read(self) -> Optional[Event]:
        """
        Read the next event from the log file.
        
        Returns:
            The next event, or None if the end of the file has been reached.
        """
        try:
            return Event.read_from(self.f)
        except EOFError:
            return None


class LogWriter:
    """
    Utility class for writing LCM log file events in order.
    """
    
    def __init__(self, filename: str):
        self._filename = filename
        
        self._f = None  # File handle
        
    @property
    def f(self):
        """
        Get the file. If not already open, open for writing.
        """
        if self._f is None:
            self._f = open(self._filename, 'wb')
        return self._f
    
    def __del__(self):
        """
        Close the file, if it exists.
        """
        if self._f is not None:
            self._f.close()
    
    def write(self, event: Event):
        """
        Write an event to the log file.
        
        Args:
            event: Event to write.
        """
        event.write_to(self.f)
