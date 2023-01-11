#!/usr/bin/env python3
from loadconf import Config


class NoBaseDirExists(Exception):
    """Exception raised when user has a base directory set
    but it does not exist.
    """

    def __init__(self, conf_file, message="ERROR: Base directory is set to"):
        self.file = conf_file
        self.message = message

    def __str__(self):
        return f'{self.message} "{self.file}" which does not exist'


class NoBaseDir(Exception):
    """Exception raised when user has not set a base directory"""

    def __init__(self, conf_file, message="ERROR: Base directory not set in"):
        self.file = conf_file
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} "{self.file}"'


def get_user_settings(program, args):
    # Create user object to read files and get settings
    user = Config(program=program)
    # Define some basic settings, files, etc.
    user_settings = {
        "prompt_cmd": "fzf",
        "prompt_args": "",
        "max_history": 20,
        "debug": False,
    }
    config_files = {
        "conf_file": "dmenuplaylist.conf",
        "playlist_file": "playlist.json",
        "playlist_bak_file": "playlist.json.bak",
    }
    files = [
        "conf_file",
        "playlist_file",
    ]
    settings = list(user_settings.keys())
    # Fill out user object
    user.define_settings(settings=user_settings)
    user.define_files(user_files=config_files)
    user.create_files(create_files=files)
    user.read_conf(user_settings=settings, read_files=["conf_file"])

    return user, args
