"""Message module"""
from __future__ import annotations
from typing import Dict, Optional
from nwutils.torch import tr_detach_data
import torch as tr

class Message:
    """
    Message class used to pass information between edges
    Parameters:
    content The content of the message
    source The string source of the message (usually the edge name)
    timestamp The timestmap when the message was sent. Defaults to 0.
    path The path of the message. Defaults to None.
    metadata Additional use-case specific metadata of the message. Not used in the (default) comparison, subclass
        this class with the use-case specific messages if needed.
    """
    def __init__(self, content: tr.Tensor, source: str = None, timestamp: int = 0,
                 path: Dict[str, tr.Tensor] = None, metadata: Optional[Dict] = None):
        assert isinstance(content, tr.Tensor), f"Wrong type: {type(content)}"
        metadata = {} if metadata is None else metadata
        path = {} if path is None else path
        if len(path) > 0:
            assert source is not None, "Path provided, but no source."
            last_key = tuple(path.keys())[-1]
            assert last_key == source, f"Path provided, but lasst path ({last_key}) differs from source ({source})"

        self.content = content
        self._timestamp = timestamp
        self._metadata = tr_detach_data(metadata)
        self._source = tr_detach_data(source)
        self._path = path
        self._hash = None

    @property
    def timestamp(self) -> int:
        """Gets the timestamp of this message"""
        return self._timestamp

    @property
    def metadata(self) -> Dict:
        """Gets the metadata of this message"""
        return self._metadata

    @property
    def source(self) -> str:
        """Gets the source of this message"""
        return self._source

    @property
    def path(self) -> str:
        """Gets the path of this message"""
        return self._path

    def equal_without_content(self, source: str, input_content: tr.Tensor) -> bool:
        """Checks if two message inputs are the same (useful for deduplication when we know it'll lead to same msg)"""
        if self.source != source:
            return False
        if len(self.path) == 0:
            return False
        last_source = tuple(self.path.keys())[-1]
        last_content = self.path[last_source]
        if last_content.shape != input_content.shape:
            return False
        return tr.allclose(last_content, input_content)

    def __repr__(self) -> str:
        return f"M(s={self.source}|c={tuple(self.content.shape)}|t={self.timestamp}|pth={len(self.path)})"

    def __str__(self) -> str:
        f_str = "Message."
        f_str += f"\n- Source: {self.source}"
        f_str += f"\n- Content: {tuple(self.content.shape)}"
        f_str += f"\n- Timestamp: {self.timestamp}"
        path = " -> ".join([f'{k}: {tuple(v.shape)}' for k, v in self.path.items()])
        f_str += f"\n- Path ({len(self.path)}): {path}"
        metadata = "yes" if len(self.metadata) > 0 else "no"
        f_str += f"\n- Metadata: {metadata}"
        return f_str

    def __eq__(self, other: Message):
        """These are so we can use sets in the graph library to add unique nodes only. Metadata is not checked!"""
        if self.source != other.source:
            return False
        if self.content.shape != other.content.shape:
            return False
        return tr.allclose(self.content, other.content)
