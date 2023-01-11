#!/usr/bin/env python3
import json
import sys
from .prompts import user_choice, InvalidCmdPrompt, InputError
from .system import open_process


def add_files(user, add):
    """
    Add the given list of args to the users playlist file.
    """
    with open(user.files["playlist_file"], "r") as data:
        playlist = json.load(data)
    playlist.extend(add)
    with open(user.files["playlist_file"], "w") as data:
        json.dump(playlist, data, indent=4)
    return 0


def ask_user(options, user, prompt):
    """
    Ask a user something and handle any errors, return False if the user
    reponds with nothing or error is caught
    """
    try:
        choice = user_choice(options=options, user=user, prompt=prompt)
    except (InvalidCmdPrompt, InputError, KeyboardInterrupt) as err:
        print(err, sys.stderr)
        return False
    if choice is None:
        return False
    return choice


def delete_item(user, item):
    """
    Delete the given item from user's playlist.
    """
    with open(user.files["playlist_file"], "r") as data:
        playlist = json.load(data)
    if item not in playlist:
        print(f"WARNING: {item} is not in your playlist", file=sys.stderr)
        return 1
    playlist.remove(item)
    with open(user.files["playlist_file"], "w") as data:
        json.dump(playlist, data, indent=4)
    return 0


def display_playlist(user, ask=True):
    """
    Display users playlist
    """
    with open(user.files["playlist_file"], "r") as data:
        playlist = json.load(data)
    if ask:
        choice = ask_user(options=playlist, user=user, prompt="Play: ")
        if not choice:
            return 1
        playlist.remove(choice)
        cmd = mpv_cmd(item=[choice], items=playlist)
    else:
        cmd = mpv_cmd(item=playlist)
    open_process(opener=cmd)
    return 0


def mpv_cmd(item, items=None):
    """
    Return a command list to feed to system.open_process
    if a path to the item is given it the two will be joined
    """
    mpv_list = [
        "mpv",
        "--script-opts=dmenuplaylist-enabled=yes",
        "--loop-playlist=no",
        "--keep-open=no",
    ]
    if items is not None:
        item.extend(items)
    mpv_list.extend(item)
    return mpv_list


def remove_item(user):
    """
    Remove selected items from user's playlist
    """
    with open(user.files["playlist_file"], "r") as data:
        playlist = json.load(data)
    choice_flag = True
    while choice_flag:
        choice = ask_user(options=playlist, user=user, prompt="Play: ")
        if not choice:
            choice_flag = False
            continue
        playlist.remove(choice)
    with open(user.files["playlist_file"], "w") as data:
        json.dump(playlist, data, indent=4)
    return 0
