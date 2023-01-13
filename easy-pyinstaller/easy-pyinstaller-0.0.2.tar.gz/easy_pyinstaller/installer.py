import os
import platform

class InstallerError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"InstallerError: {self.message}"

class Installer:
    def __init__(self, file:str, paths:list):
        self.paths = ":".join(paths)
        self.file = file

        if os.path.isfile(self.file) and os.path.splitext(self.file)[1] == ".py":
            self.execute()
        else:
            raise InstallerError("Python file not found")

    def execute(self):
        command = f"{self.python_command()} pyinstaller --onefile {self.file} {f' -p {self.paths}' if len(self.paths) > 0 else ''}"

        os.system(command)

    def python_command(self):
        if platform.system() == 'Windows':
            return 'py'
        return 'python3'
