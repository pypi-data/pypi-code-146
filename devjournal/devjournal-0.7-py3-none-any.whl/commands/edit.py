from devjournal.edit import edit_existing_file_with_editor
from devjournal.entry import get_entry_path


def edit(id_: int):
    edit_existing_file_with_editor(get_entry_path(id_))
