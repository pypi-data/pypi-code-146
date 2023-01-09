from dataclasses import dataclass
from typing import BinaryIO


ENDIANNESS = 'big'
STRING_ENCODING = 'utf-8'
SYNCWORD_BYTES = 4
LCM_SYNCWORD = (0xEDA1DA01).to_bytes(SYNCWORD_BYTES, ENDIANNESS)
EVENT_NUMBER_BYTES = 8
TIMESTAMP_BYTES = 8
CHANNEL_LENGTH_BYTES = 4
DATA_LENGTH_BYTES = 4
HEADER_BYTES = SYNCWORD_BYTES + EVENT_NUMBER_BYTES + TIMESTAMP_BYTES + CHANNEL_LENGTH_BYTES + DATA_LENGTH_BYTES


class BadSyncError(Exception):
    """
    Exception raised when event header read is out of sync.
    """
    def __init__(self, syncword, start_byte: int) -> None:
        super().__init__('Bad syncword {} at byte {}'.format(syncword, start_byte))


@dataclass
class Header:
    """
    LCM event header.
    """
    event_number: int
    timestamp: int
    channel_length: int
    data_length: int
    
    @classmethod
    def read_from(cls, f: BinaryIO) -> 'Header':
        """
        Read a header from a file.
        
        Args:
            f: File to read from.
        
        Returns:
            Parsed LCM header.
        """
        start_byte = f.tell()
        
        # Check the syncword
        syncword = f.read(SYNCWORD_BYTES)
        if len(syncword) == 0:
            raise EOFError()
        elif syncword != LCM_SYNCWORD:
            raise BadSyncError(syncword, start_byte)
        
        # Read header data
        event_number = int.from_bytes(f.read(EVENT_NUMBER_BYTES), ENDIANNESS)
        timestamp = int.from_bytes(f.read(TIMESTAMP_BYTES), ENDIANNESS)
        channel_length = int.from_bytes(f.read(CHANNEL_LENGTH_BYTES), ENDIANNESS)
        data_length = int.from_bytes(f.read(DATA_LENGTH_BYTES), ENDIANNESS)
        
        # Compose the header object
        return cls(event_number, timestamp, channel_length, data_length)
    
    def write_to(self, f: BinaryIO):
        """
        Write to a file.
        
        Args:
            f: File to write to.
        """
        f.write(LCM_SYNCWORD)
        f.write(self.event_number.to_bytes(EVENT_NUMBER_BYTES, ENDIANNESS))
        f.write(self.timestamp.to_bytes(TIMESTAMP_BYTES, ENDIANNESS))
        f.write(self.channel_length.to_bytes(CHANNEL_LENGTH_BYTES, ENDIANNESS))
        f.write(self.data_length.to_bytes(DATA_LENGTH_BYTES, ENDIANNESS))

@dataclass
class Event:
    """
    LCM event.
    """
    header: Header
    channel: str
    data: bytes
    
    @classmethod
    def read_from(cls, f: BinaryIO) -> 'Event':
        """
        Read an event from a file.
        
        Args:
            f: File to read from.
        
        Returns:
            Parsed LCM event.
        """
        # Read the header. This will raise an exception if the syncword is bad.
        header = Header.read_from(f)
        
        # Read the channel name
        channel = f.read(header.channel_length).decode(STRING_ENCODING)
        
        # Read the data
        data = f.read(header.data_length)
        
        # Compose the event object
        return cls(header, channel, data)
    
    def write_to(self, f: BinaryIO):
        """
        Write to a file.
        
        Args:
            f: File to write to.
        """
        self.header.write_to(f)
        f.write(self.channel.encode(STRING_ENCODING))
        f.write(self.data)
