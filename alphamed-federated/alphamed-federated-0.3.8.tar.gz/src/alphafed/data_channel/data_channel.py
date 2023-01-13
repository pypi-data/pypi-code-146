"""计算参与方之间传输数据的数据通道."""

from abc import ABC, abstractmethod
from typing import List, Optional, Union

from ..contractor import ApplySendingDataEvent

__all__ = ['DataChannel', 'SendingError']


class DataChannel(ABC):
    """数据传输通道."""

    @abstractmethod
    def send_stream(self,
                    source: str,
                    target: Union[str, List[str]],
                    data_stream: bytes,
                    connection_timeout: int = 30,
                    timeout: int = 60,
                    **kwargs) -> Optional[List[str]]:
        """Send data stream to receivers.

        Args:
            source:
                the ID of the data sender.
            target:
                the ID or ID list of receivers.
            data_stream:
                data_stream content.
            connection_timeout:
                the timeout seconds to establish the connection.
            timeout:
                the timeout seconds to complete the data transmission, set to 0 to disable timeout.

        Return:
            (Optional) the ID list of accepting nodes
        """

    @abstractmethod
    def receive_stream(self,
                       apply_event: ApplySendingDataEvent,
                       receiver: str = None,
                       **kwargs) -> bytes:
        """Receive data stream from a sender.

        Args:
            apply_event:
                the ApplySendingDataEvent object of this data transmission.
            receiver:
                the ID of the receiver.
        """


class SendingError(Exception):
    ...
