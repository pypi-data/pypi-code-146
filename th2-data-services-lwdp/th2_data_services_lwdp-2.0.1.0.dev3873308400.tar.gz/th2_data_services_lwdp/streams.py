from typing import List

from th2_grpc_common.common_pb2 import Direction
from th2_grpc_lw_data_provider.lw_data_provider_pb2 import MessageStream


class Stream:
    """General interface for stream for lwdp ds.

    The class gives the opportunity to make stream with direction.
    """

    def __init__(self, alias: str, direction: str = None):
        """Streams constructor.

        Args:
            alias: Stream name.
            direction: Direction of Stream (Only 1 or 2). If None then is both directions.
        """
        self._alias = alias
        if direction is not None:
            direction = direction.upper()
            if direction not in ("1", "2"):
                raise ValueError("The direction must be '1' or '2'.")
        self._direction = direction

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(" f"alias={self._alias}, " f"direction={self._direction})"

    def url(self) -> str:
        """Generates the stream part of the HTTP protocol API.

        Returns:
            str: Generated streams.
        """
        if self._direction is None:
            return f"&stream={self._alias}"
        return f"&stream={self._alias}:{self._direction}"

    # +TODO - Fix it when we need grpc
    def grpc(self) -> MessageStream:
        """Generates the grpc object of the GRPC protocol API.

        Returns:
            MessageStream: Stream with specified direction.
        """
        if self._direction is None:
            return [
                MessageStream(name=self._alias, direction=Direction.FIRST),
                MessageStream(name=self._alias, direction=Direction.SECOND),
            ]
            return result
        return [
            MessageStream(name=stream, direction=Direction.Value(self._direction))
            for stream in self._aliases
        ]


class Streams:
    """General interface for composite streams of lwdp ds.

    The class gives the opportunity to make list of streams with direction for each.
    """

    def __init__(self, aliases: List[str], direction: str = None):
        """Streams constructor.

        Args:
            aliases: List of Streams.
            direction: Direction of Streams (Only 1 or 2). If None then is both directions.
        """
        self._aliases = aliases
        if direction is not None:
            direction = direction.upper()
            if direction not in ("1", "2"):
                raise ValueError("The direction must be '1' or '2'.")
        self._direction = direction

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(" f"aliases={self._aliases}, " f"direction={self._direction})"

    def as_list(self):
        result = []
        if self._direction is None:
            for alias in self._aliases:
                result.append(alias)
        else:
            for alias in self._aliases:
                result.append(f"{alias}:{self._direction}")
        return result

    def url(self) -> str:
        """Generates the stream part of the HTTP protocol API.

        Returns:
            str: Generated streams.
        """
        if self._direction is None:
            return "&".join([f"stream={alias}" for alias in self._aliases])
        return "&".join([f"stream={stream}:{self._direction}" for stream in self._aliases])

    def grpc(self) -> List[MessageStream]:
        """Generates the grpc objects of the GRPC protocol API.

        Returns:
            List[MessageStream]: List of Stream with specified direction.
        """
        if self._direction is None:
            result = []
            for stream in self._aliases:
                result += [
                    MessageStream(name=stream, direction=Direction.FIRST),
                    MessageStream(name=stream, direction=Direction.SECOND),
                ]
            return result
        return [
            MessageStream(name=stream, direction=Direction.Value(self._direction))
            for stream in self._aliases
        ]
