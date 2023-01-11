import subprocess
from tempfile import NamedTemporaryFile
from pathlib import Path
import shutil
import os
import importlib
import re

COMMANDS = [['sensible-editor'], ['open', '-W']]
PYTHON_VERSION = (3, 6, 5)


def editor(arg):
    with NamedTemporaryFile() as tempfile:
        Path(tempfile.name).write_text(arg)
        command = [os.environ.get('EDITOR')]
        if not command[0] or not shutil.which(command[0]):
            iterator = (c for c in COMMANDS if shutil.which(c[0]))
            command = next(filter(None, iterator), None)
            if not command:
                raise RuntimeError("The manage command required an editor")
        subprocess.run(command + [tempfile.name])
        return Path(tempfile.name).read_text()

def do_import(folder_path, module_base):
    for import_file in folder_path.iterdir():
        if re.match(r'^[^_].*\.py$', import_file.name):
            importlib.import_module(f'{module_base}.{import_file.stem}')
