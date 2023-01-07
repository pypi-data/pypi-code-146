import devjournal.entry
from devjournal.entry import get_ids_and_entries


def log():
    devjournal.entry.print_ids_and_entries(get_ids_and_entries())
