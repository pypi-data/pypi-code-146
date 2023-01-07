import devjournal.entry
from devjournal.entry import get_ids_and_entries


def find(words: list[str]):
    ids_and_entries = [
        (i, entry)
        for i, entry in get_ids_and_entries()
        if any(word in entry.text for word in words)
    ]
    devjournal.entry.print_ids_and_entries(ids_and_entries)
