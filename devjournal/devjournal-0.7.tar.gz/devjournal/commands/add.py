from datetime import datetime

from devjournal.constants import entries_directory, filename_from_datetime
from devjournal.edit import create_new_file_with_editor


def add(text: str | None = None):
    entries_directory().mkdir(parents=True, exist_ok=True)
    entry_file = entries_directory() / filename_from_datetime(datetime.now())
    if text:
        entry_file.write_text(text)
    else:
        create_new_file_with_editor(entry_file)
