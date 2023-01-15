from pathlib import Path


def find_missed_drafts() -> bool:
    drafts = Path("docs/drafts")
    numbers = {int(draft.stem) for draft in drafts.glob("*.md")}
    expected = set(range(1, len(numbers) + 1))
    return numbers != expected
