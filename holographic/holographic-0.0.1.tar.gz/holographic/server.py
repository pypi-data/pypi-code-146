from typing import Dict, Iterable, List
import uuid

from flask import Flask, request

from .models import (
    ChannelEvent,
    EventAction,
    FileState,
)


class ClientError(Exception):
    def __init__(self, message: str):
        self.message = message

class NotFoundError(Exception):
    def __init__(self, message: str):
        self.message = message

class Channel:
    def __init__(self, id: str):
        self.id = id
        self.all_files: Dict[str, FileState] = {}
        self.updates: Dict[str, ChannelEvent] = {}

    def __repr__(self) -> str:
        num_files = len(self.all_files)
        unretrieved_updates = len(self.updates)
        return f"<Channel ({self.id}) files: {num_files}  updates: {unretrieved_updates}>"

    def new_events(self, events: Iterable[ChannelEvent]) -> None:
        for e in events:
            if e.action in [EventAction.CREATE, EventAction.UPDATE]:
                self.all_files[e.filepath] = FileState.from_channel_event(e)
                if e.filepath in self.updates:
                    old_event = self.updates[e.filepath]
                    old_event.action = EventAction.UPDATE
                    old_event.contents = e.contents
                    old_event.nonce = e.nonce
                else:
                    self.updates[e.filepath] = e
            if e.action == EventAction.DELETE:
                if e.filepath in self.all_files:
                    del self.all_files[e.filepath]
                if e.filepath in self.updates:
                    old_event = self.updates[e.filepath]
                    old_event.action = EventAction.DELETE
                    old_event.contents = e.contents
                    old_event.nonce = e.nonce

    def get_updates(self) -> List[ChannelEvent]:
        updates = list(self.updates.values())
        self.updates = {}
        return updates

    def get_all_files(self) -> List[FileState]:
        return list(self.all_files.values())

class EventStore:
    def __init__(self):
        # Holds the events that haven't been retrieved yet
        self.channels: Dict[str, Channel] = {}

    def new_channel(self):
        channel_id = str(uuid.uuid4())
        self.channels[channel_id] = Channel(channel_id)
        return channel_id

    def update_channel(self, channel_id: str, events: Iterable[ChannelEvent]):
        if channel_id not in self.channels:
            raise NotFoundError(f"There is no channel with id '{channel_id}'.")
        self.channels[channel_id].new_events(events)
        
    def get_channel_updates(self, channel_id: str) -> List[ChannelEvent]:
        if channel_id not in self.channels:
            raise NotFoundError(f"There is no channel with id '{channel_id}'.")
        return self.channels[channel_id].get_updates()

    def get_all_files_from_channel(self, channel_id: str) -> List[FileState]:
        if channel_id not in self.channels:
            raise NotFoundError(f"There is no channel with id '{channel_id}'.")
        return self.channels[channel_id].get_all_files()

    def close_channel(self, channel_id: str):
        if channel_id not in self.channels:
            raise NotFoundError(f"There is no channel with id '{channel_id}'.")
        del self.channels[channel_id]


app = Flask(__name__)
event_store = EventStore()

@app.get("/channel/<channel_id>/updates")
def get_updates_route(channel_id):
   return get_channel_updates(channel_id)

@app.route("/channel/<channel_id>", methods=["GET", "POST", "DELETE"])
def channel_route(channel_id):
    try:
        if request.method == "GET":
            return get_channel_state(channel_id)
        elif request.method == "POST":
            return update_channel(channel_id)
        elif request.method == "DELETE":
            return close_channel(channel_id)
        else:
            return "Method not allowed", 405
    except ClientError as e:
        return e.message, 400
    except NotFoundError as e:
        return e.message, 404

@app.post("/channel")
def new_channel_route():
    return new_channel()

def new_channel():
    global event_store
    channel_id = event_store.new_channel()
    return channel_id

def close_channel(channel_id):
    global event_store
    event_store.close_channel(channel_id)
    return ""

def update_channel(channel_id):
    global event_store
    body_json = request.json
    if body_json is None:
        return "Body was not valid JSON.", 400
    raw_events: List[dict] = body_json
    events = [ChannelEvent.from_dict(e) for e in raw_events]
    event_store.update_channel(channel_id, events)
    return ""

def get_channel_state(channel_id) -> List[dict]:
    global event_store
    files = [f.to_dict() for f in event_store.get_all_files_from_channel(channel_id)]
    return files

def get_channel_updates(channel_id) -> List[dict]:
    global event_store
    updates = [u.to_dict() for u in event_store.get_channel_updates(channel_id)]
    return updates


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=7788, debug=True)