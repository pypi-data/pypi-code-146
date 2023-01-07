from devjournal.entry import get_entry_path


def delete(id_: int):
    get_entry_path(id_).unlink()
