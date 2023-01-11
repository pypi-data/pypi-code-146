import os.path

VERSION_FILE = os.path.join(os.path.dirname(__file__), "local_version.txt")
if os.path.isfile(VERSION_FILE):
    with open(VERSION_FILE) as f:
        __version__ = f.read().strip()
