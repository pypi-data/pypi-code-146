import base64
from enum import Enum
import json

from pydantic import BaseModel

class EventAction(Enum):
    CREATE="CREATE"
    DELETE="DELETE"
    UPDATE="UPDATE"

class ChannelEvent(BaseModel):
    filepath: str
    action: EventAction
    contents: bytes
    nonce: bytes

    def to_dict(self) -> dict:
        return {
            "filepath": self.filepath,
            "action": self.action.value,
            "contents": base64.b64encode(self.contents).decode(),
            "nonce": base64.b64encode(self.nonce).decode(),
        }

    @classmethod
    def from_dict(cls, d: dict):
        action: EventAction
        raw_action = d["action"]
        if raw_action == "CREATE":
            action = EventAction.CREATE
        elif raw_action == "DELETE":
            action = EventAction.DELETE
        elif raw_action == "UPDATE":
            action = EventAction.UPDATE
        else:
            raise ValueError(f"Bad value for action: {raw_action}")
        return cls(
            filepath=d["filepath"],
            action=action,
            contents=base64.b64decode(d["contents"].encode()),
            nonce=base64.b64decode(d["nonce"].encode()),
        )

class FileState(BaseModel):
    filepath: str
    contents: bytes
    nonce: bytes

    @classmethod
    def from_channel_event(cls, e: ChannelEvent) -> "FileState":
        return cls(
            filepath=e.filepath,
            contents=e.contents,
            nonce=e.nonce,
        )

    def to_dict(self) -> dict:
        return {
            "filepath": self.filepath,
            "contents": base64.b64encode(self.contents).decode(),
            "nonce": base64.b64encode(self.nonce).decode(),
        }

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            filepath=d["filepath"],
            contents=base64.b64decode(d["contents"].encode()),
            nonce=base64.b64decode(d["nonce"].encode()),
        )
