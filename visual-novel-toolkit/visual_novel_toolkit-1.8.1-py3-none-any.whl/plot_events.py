from collections import defaultdict
from itertools import pairwise
from pathlib import Path
from string import ascii_lowercase

from yaml import CSafeLoader
from yaml import load

from .types import Events


def plot_events() -> None:
    data = Path("data")
    events_file = data / "events.yml"

    events: Events = load(events_file.read_text(), Loader=CSafeLoader)

    docs = Path("docs")
    docs.mkdir(exist_ok=True)

    mermaid_file = docs / "events.mmd"
    mermaid_file.write_text(plot(events))


def plot(events: Events) -> str:
    ids = lookup()

    lines = ["flowchart BT"]

    for group_name, event_list in events.items():
        lines.append(f"  subgraph {group_name}")
        lines.append("    direction BT")
        for event_name in event_list:
            lines.append(f"    {ids[event_name]}[{event_name}]")
        lines.append("  end")
        lines.append("")

    for event_list in events.values():
        for left, right in pairwise(event_list):
            lines.append(f"  {ids[left]} --> {ids[right]}")

    return "\n".join(lines)


def lookup() -> dict[str, str]:
    gen = iter(ascii_lowercase)
    return defaultdict(lambda: next(gen))
