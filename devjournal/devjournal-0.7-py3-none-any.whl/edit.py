import os
import subprocess
from pathlib import Path


def create_new_file_with_editor(file_path: Path):
    file_path.touch()
    try:
        edit_existing_file_with_editor(file_path)
        text_in_file = file_path.read_text()
        assert text_in_file
    except Exception:
        print("File empty, entry aborted.")
        file_path.unlink()


def edit_existing_file_with_editor(file_path: Path):
    command = [editor] if (editor := os.getenv("EDITOR")) else ["start", "/WAIT"]
    process = subprocess.Popen(
        command + [str(file_path).replace("\\", "/")], shell=True
    )
    process.wait()
