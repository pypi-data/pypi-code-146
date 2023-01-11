import base64
import os
from pathlib import Path
import textwrap
import time
import secrets
from typing import (
    Tuple,
    List,
    Union,
    Dict,
)

import click
from cryptography.hazmat.primitives.ciphers.aead import AESOCB3
from pydantic import BaseModel
import requests
from rich.text import Text
from rich.console import Console
from rich.syntax import Syntax

from .models import (
    ChannelEvent,
    EventAction,
)


class FileAdd(BaseModel):
    path: str
    contents: str

    def to_channel_event(self, encryptor: AESOCB3) -> ChannelEvent:
        contents, nonce = encrypt_contents(encryptor, self.contents.encode(), self.path.encode())
        return ChannelEvent(
            filepath=self.path,
            action=EventAction.CREATE,
            contents=contents,
            nonce=nonce,
        )

class FileDelete(BaseModel):
    path: str

    def to_channel_event(self, encryptor: AESOCB3) -> ChannelEvent:
        # Generate some cryptographically random contents so that we
        # don't use an empty string every time for delete actions. I suspect
        # that using the same contents every time for delete actions
        # may make it easier to guess the key given that the cyphertext
        # will then only be derived from the key, the nonce, and the associated data,
        # where both the nonce and the associated data are public.
        random_contents = secrets.token_bytes(128)
        contents, nonce = encrypt_contents(encryptor, random_contents, self.path.encode())
        return ChannelEvent(
            filepath=self.path,
            action=EventAction.DELETE,
            contents=contents,
            nonce=nonce,
        )


class FileUpdate(BaseModel):
    path: str
    contents: str

    def to_channel_event(self, encryptor: AESOCB3) -> ChannelEvent:
        contents, nonce = encrypt_contents(encryptor, self.contents.encode(), self.path.encode())
        return ChannelEvent(
            filepath=self.path,
            action=EventAction.UPDATE,
            contents=contents,
            nonce=nonce,
        )


def encrypt_contents(encryptor: AESOCB3, contents: bytes, associated_data: bytes) -> Tuple[bytes, bytes]:
    """
    Encrypts the contents and returns a tuple of <encrypted_contents> and
    <nonce>.
    """
    nonce = os.urandom(12)
    cyphertext = encryptor.encrypt(nonce, contents, associated_data)
    return cyphertext, nonce


class File(BaseModel):
    path: str
    last_modified: float
    contents: str


# http://127.0.0.1:7788

@click.command()
@click.argument("url")
@click.argument("target_dir")
def main(url, target_dir):
    console = Console()
    channel_id = ""
    try:
        channel_id = open_channel(url)
        watch_and_emit(url, channel_id, target_dir)
    except KeyboardInterrupt:
        if channel_id != "":
            close_channel(url, channel_id)
        console.print("\nTransmission ended.", style="bold")
        

def watch_and_emit(url: str, channel_id: str, target_dir_arg: str):
    target_dir = Path(target_dir_arg)
    if not target_dir.exists():
        raise ValueError(f"Direcotry '{str(target_dir)}' does not exist.")
    target_dir = os.path.abspath(target_dir) + "/"
    # Instantiate the encryption machinery
    key = AESOCB3.generate_key(bit_length=256)
    encryptor = AESOCB3(key)
    print_channel_details(url, channel_id, key)
    poll_interval_ms = 750
    old_files_set = set()
    files_map: Dict[str, File] = {}
    while True:
        events: List[Union[FileAdd, FileUpdate, FileDelete]] = []
        new_files_set = set()
        for dirpath, _, filenames in os.walk(target_dir):
            for filename in filenames:
                abs_path = os.path.abspath(os.path.join(dirpath, filename))
                # In the destination filesystem we want to write the contents of `target_dir`, not the
                # directory its self or any of its ancestors. So to get the filepath as it should be
                # consumed by the remote system we need to remove the path to the target directory from
                # the paths of the files in the directory. The resulting path is `holograph_path`. e.g.
                # if there is a file in target_dir whose absolute path is 
                # '/user/grandparent/parent/target_dir/package1/module1.py', this file will be transmitted
                # to the server with the path 'package1/module1.py'.
                holograph_path = abs_path.replace(target_dir, "")
                new_files_set.add(holograph_path)
                # Check if this file existed last time we polled
                if holograph_path in files_map:
                    old_file_info = files_map[holograph_path]
                    # it did
                    # check if it's been updated
                    last_updated = os.path.getmtime(abs_path)
                    if last_updated == old_file_info.last_modified:
                        # nope
                        continue
                    # yep, update the info in the files_map
                    with open(abs_path) as h:
                        contents = h.read()
                    files_map[holograph_path] = File(
                        path=holograph_path,
                        last_modified=last_updated,
                        contents=contents,
                    )
                    events.append(FileUpdate(
                        path=holograph_path,
                        contents=contents,
                    ))
                else:
                    # this is a new file, create a new entry in the file map
                    last_updated = os.path.getmtime(abs_path)
                    with open(abs_path) as h:
                        contents = h.read()
                    files_map[holograph_path] = File(
                        path=holograph_path,
                        last_modified=last_updated,
                        contents=contents,
                    )
                    events.append(FileAdd(
                        path=holograph_path,
                        contents=contents,
                    ))
        # now check which files have been deleted
        deleted_file_paths = old_files_set - new_files_set
        for deleted_path in deleted_file_paths:
            del files_map[deleted_path]
            events.append(FileDelete(path=deleted_path))
        old_files_set = new_files_set
        if len(events) > 0:
            emit_events(url, channel_id, events, encryptor)
        time.sleep(poll_interval_ms / 1000)

def emit_events(url: str, channel_id: str, events: List[Union[FileAdd, FileUpdate, FileDelete]], encryptor: AESOCB3):
    event_objs = [e.to_channel_event(encryptor).to_dict() for e in events]
    response = requests.post(f"{url}/channel/{channel_id}", json=event_objs)
    response.raise_for_status()

def open_channel(url: str) -> str:
    response = requests.post(f"{url}/channel", json={})
    response.raise_for_status()
    return response.text

def close_channel(url: str, channel: str):
    response = requests.delete(f"{url}/channel/{channel}")
    response.raise_for_status()

def print_channel_details(url: str, channel: str, key: bytes):
    """
    Prints the channel details in a format that can simply be copied into the 
    target python script.
    """
    encoded_key = base64.b64encode(key).decode()
    code_snippet = textwrap.dedent(f'''
    
    import holograph

    holograph.tune_in(
        key="{encoded_key}",
        url="{url}",
        channel="{channel}",
    )

    ''')
    console = Console()
    intro_message = Text("Tune in from your remote location using the following code which ", style="bold")
    intro_message.append("must be kept secret for the duration of your session", style="bold red")
    intro_message.append(":")
    console.print(intro_message)
    syntax = Syntax(code_snippet, "python", background_color="default")
    console.print(syntax)
    console.print("Transmitting file updates... ", style="bold")

if __name__ == "__main__":
    main()